// Copyright (c) 2012, the Dart project authors.  Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

/** Collects several code emitters for the template tool. */
// TODO(sigmund): add visitor that applies all emitters on a component
// TODO(sigmund): add support for conditionals, so context is changed at that
// point.
library emitters;

import 'package:html5lib/dom.dart';
import 'package:html5lib/dom_parsing.dart';
// TODO(jmesserly): this utility should be somewhere else.
import 'package:html5lib/src/utils.dart' show reversed;

import 'code_printer.dart';
import 'codegen.dart' as codegen;
import 'file_system/path.dart';
import 'files.dart';
import 'html5_utils.dart';
import 'html5_setters.g.dart';
import 'info.dart';
import 'messages.dart';
import 'utils.dart';

/**
 * An emitter for a web component feature.  It collects all the logic for
 * emitting a particular feature (such as data-binding, event hookup) with
 * respect to a single HTML element.
 */
abstract class Emitter<T extends NodeInfo> {
  /** Information about the element for which code is being emitted. */
  final T info;

  Emitter(this.info);

  /** Emit declarations needed by this emitter's feature. */
  void emitDeclarations(Context context) {}

  /** Emit feature-related statemetns in the `created` method. */
  void emitCreated(Context context) {}

  /** Emit feature-related statemetns in the `inserted` method. */
  void emitInserted(Context context) {}

  /** Emit feature-related statemetns in the `removed` method. */
  void emitRemoved(Context context) {}

  // The following are helper methods to make it simpler to write emitters.
  Context contextForChildren(Context context) => context;

  /** Generates a unique Dart identifier in the given [context]. */
  String newName(Context context, String prefix) =>
      '${prefix}${context.scope.newId()}';
}

/**
 * Context used by an emitter. Typically representing where to generate code
 * and additional information, such as total number of generated identifiers.
 */
class Context {
  final CodePrinter declarations;
  final CodePrinter createdMethod;
  final CodePrinter insertedMethod;
  final CodePrinter removedMethod;

  final LifecycleScope scope;
  Messages _messages = new Messages.silent();
  
  /**
   * If [messages] is null, sets a new silent instance of [Messages]
   */
  set messages(Messages messages) {
    messages = messages == null ? new Messages.silent() : messages;
    _messages = messages; 
  }
  
  Messages get messages => _messages;

  Context([CodePrinter declarations,
           CodePrinter createdMethod,
           CodePrinter insertedMethod,
           CodePrinter removedMethod,
           LifecycleScope scope])
      : this.declarations = getOrCreatePrinter(declarations),
        this.createdMethod = getOrCreatePrinter(createdMethod),
        this.insertedMethod = getOrCreatePrinter(insertedMethod),
        this.removedMethod = getOrCreatePrinter(removedMethod),
        this.scope = getOrCreateScope(scope);

  static getOrCreatePrinter(CodePrinter p) => p != null ? p : new CodePrinter();
  static getOrCreateScope(LifecycleScope s) =>
      s != null ? s : new LifecycleScope();
}

/**
 * Represents information about the current lifecycle scope in the template
 * tree. Simple templates without conditionals or iteration will have a single
 * scope because the whole template has a single lifecycle. Conditionals and
 * iteration introduce new scopes where data-bindings and events within the
 * conditions or loops have a different lifetime. The emitters use lifecycle
 * scopes to group together watchers that have the same lifecycle.
 */
class LifecycleScope {
  /** Enclosing scope, used mainly to compute unique names on nested scopes. */
  LifecycleScope parent;

  /**
   * Name of a variable that holds a list of all stoppers of watchers in this
   * lifecycle scope.
   */
  String stoppersName;

  LifecycleScope([this.parent]);

  // TODO(sigmund): track watch expressions used - maybe we can combine them
  // into a single watcher.

  int _totalIds = 0;
  int _nextId() => ++_totalIds;

  String newId() => _canonicalId(new StringBuffer()).toString();

  StringBuffer _canonicalId(StringBuffer buff) {
    if (parent != null) {
      parent._canonicalId(buff);
      buff.add('_');
    }
    buff.add(_nextId());
    return buff;
  }
}

/**
 * Generates a field for any element that has either event listeners or data
 * bindings.
 */
class ElementFieldEmitter extends Emitter<ElementInfo> {
  final _childrenCreated = new CodePrinter();

  ElementFieldEmitter(ElementInfo info) : super(info);

  void emitDeclarations(Context context) {
    if (!info.isRoot) {
      if (info.node.namespace == 'http://www.w3.org/2000/svg') {
        context.declarations.add('autogenerated_svg.SvgElement ${info.identifier};');
      } else {
        var type = typeForHtmlTag(info.node.tagName);
        context.declarations.add('autogenerated_$type ${info.identifier};');
      }
    }
  }

  void emitCreated(Context context) {
    var printer = context.createdMethod;

    if (info.createdInCode) {
      printer.add("${info.identifier} = ${_emitCreateHtml(info.node)};");
    } else if (!info.isRoot) {
      var parentId = '_root';
      for (var p = info.parent; p != null; p = p.parent) {
        if (p.identifier != null) {
          parentId = p.identifier;
          break;
        }
      }
      printer.add("${info.identifier} = $parentId.query('#${info.node.id}');");
    }

    printer.add(_childrenCreated);

    if (info.childrenCreatedInCode && !info.hasIterate &&
        !info.hasIfCondition) {
      for (var child in info.children) {
        var exp = _createChildExpression(child);
        printer.add("${info.identifier}.nodes.add($exp);");
      }
    }
  }

  void emitRemoved(Context context) {
    context.removedMethod.add('${info.identifier} = null;');
  }

  Context contextForChildren(Context c) => new Context(
      c.declarations, _childrenCreated, c.insertedMethod, c.removedMethod,
      c.scope);
}

/** Generates a field for any data-bound content node. */
class ContentFieldEmitter extends Emitter<TextInfo> {
  ContentFieldEmitter(TextInfo info) : super(info);

  void emitDeclarations(Context context) {
    context.declarations.add('var ${info.identifier};');
  }

  void emitCreated(Context context) {
    context.createdMethod.add(
        "${info.identifier} = new autogenerated_html.Text('');");
  }

  void emitRemoved(Context context) {
    context.removedMethod.add("${info.identifier} = null;");
  }
}


/**
 * Generates event listeners attached to a node and code that attaches/detaches
 * the listener.
 */
class EventListenerEmitter extends Emitter<ElementInfo> {

  EventListenerEmitter(ElementInfo info) : super(info);

  /** Generate a field for each listener, so it can be detached on `removed`. */
  void emitDeclarations(Context context) {
    info.events.forEach((name, events) {
      for (var event in events) {
        var listenerName = '__listener${info.identifier}_${name}_';
        event.listenerField = newName(context, listenerName);
        context.declarations.add(
          'autogenerated_html.EventListener ${event.listenerField};');
      }
    });
  }

  /** Define the listeners. */
  // TODO(sigmund): should the definition of listener be done in `created`?
  void emitInserted(Context context) {
    var elemField = info.identifier;
    info.events.forEach((name, events) {
      for (var event in events) {
        // TODO(jmesserly): use .on.camelCaseName when possible. But make sure
        // that custom events still work.
        var field = event.listenerField;
        // Note: the name $event is from AngularJS and is essentially public
        // API. See issue #175.
        context.insertedMethod.add('''
          $field = (\$event) {
            ${event.action(elemField)};
            autogenerated.dispatch();
          };
          $elemField.on.${event.eventName}.add($field);
        ''');
      }
    });
  }

  /** Emit feature-related statements in the `removed` method. */
  void emitRemoved(Context context) {
    info.events.forEach((name, events) {
      for (var event in events) {
        var field = event.listenerField;
        context.removedMethod.add('''
          ${info.identifier}.on.${event.eventName}.remove($field);
          $field = null;
        ''');
      }
    });
  }
}

/**
 * Common base class for all emitters containing some form of data binding. This
 * emitter ensures that there is a `_stoppers` variable that will hold the
 * stoppers for all watchers created by subclasses of this emitter.
 */
class DataBindingEmitter<T extends NodeInfo> extends Emitter<T> {
  DataBindingEmitter(T info) : super(info);

  bool addStopper = false;

  /** Watchers for each data binding. */
  void emitDeclarations(Context context) {
    addStopper = false;
    if (context.scope.stoppersName == null) {
      var name = newName(context, '__stoppers');
      context.declarations.add('List<autogenerated.WatcherDisposer> $name;');
      context.scope.stoppersName = name;
      addStopper = true;
    }
  }

  void emitCreated(Context context) {
    if (addStopper) {
      var name = context.scope.stoppersName;
      context.createdMethod.add('$name = [];');
    }
  }

  void emitRemoved(Context context) {
    if (addStopper) {
      var name = context.scope.stoppersName;
      context.removedMethod.add('($name..forEach((s) => s())).clear();');
    }
  }
}

/** Emitter for attributes with some form of data-binding. */
class AttributeEmitter extends DataBindingEmitter<ElementInfo> {
  AttributeEmitter(ElementInfo info) : super(info);

  void emitDeclarations(Context context) {
    // Emit _stoppers only if we will be emitting attribute bindings.
    if (info.attributes.length > 0) super.emitDeclarations(context);
  }

  /** Watchers for each attribute data binding. */
  void emitInserted(Context context) {
    var stoppers = context.scope.stoppersName;
    var printer = context.insertedMethod;
    info.attributes.forEach((name, attr) {
      if (attr.isClass) {
        _emitClassAttributeInserted(stoppers, attr, printer);
      } else if (attr.isStyle) {
        _emitStyleAttributeInserted(stoppers, attr, printer);
      } else if (attr.isSimple) {
        _emitSimpleAttributeInserted(stoppers, name, attr, printer);
      } else if (attr.isText) {
        _emitTextAttributeInserted(stoppers, name, attr, printer);
      }
    });
  }

  void _emitClassAttributeInserted(
      String stoppers, AttributeInfo attr, CodePrinter printer) {
    for (int i = 0; i < attr.bindings.length; i++) {
      var binding = attr.bindings[i];
      printer.add('$stoppers.add('
          'autogenerated.bindCssClasses(${info.identifier}, () => $binding));');
    }
  }

  void _emitStyleAttributeInserted(
      String stoppers, AttributeInfo attr, CodePrinter printer) {
    var id = info.identifier;
    var binding = attr.boundValue;
    printer.add('$stoppers.add(autogenerated.bindStyle($id, () => $binding));');
  }

  void _emitSimpleAttributeInserted(
      String stoppers, String name, AttributeInfo attr, CodePrinter printer) {
    var binding = attr.boundValue;
    var field = _findDomField(info, name);
    var exp = '__e.newValue';
    if (urlAttributes.contains(name)) {
      exp = 'autogenerated.sanitizeUri($exp)';
    }
    printer.add('$stoppers.add(autogenerated.watchAndInvoke(() => $binding, '
        '(__e) { ${info.identifier}.$field = $exp; }));');

    if (attr.customTwoWayBinding) {
      printer.add('$stoppers.add(autogenerated.watchAndInvoke(')
             .add('() => ${info.identifier}.$field, ')
             .add('(__e) { $binding = __e.newValue; }));');
    }
  }

  void _emitTextAttributeInserted(
      String stoppers, String name, AttributeInfo attr, CodePrinter printer) {
    var textContent = attr.textContent.map(escapeDartString);
    var setter = _findDomField(info, name);
    var content = new StringBuffer();
    var binding;
    if (attr.bindings.length == 1) {
      binding = attr.boundValue;
      content.add(textContent[0]);
      content.add('\${__e.newValue}');
      content.add(textContent[1]);
    } else {
      // TODO(jmesserly): we could probably do something faster than a list
      // for watching on multiple bindings.
      binding = '[${Strings.join(attr.bindings, ", ")}]';

      for (int i = 0; i < attr.bindings.length; i++) {
        content.add(textContent[i]);
        content.add("\${__e.newValue[$i]}");
      }
      content.add(textContent.last);
    }

    var exp = "'$content'";
    if (urlAttributes.contains(name)) {
      exp = 'autogenerated.sanitizeUri($exp)';
    }
    printer.add("$stoppers.add(autogenerated.watchAndInvoke(() => $binding, "
        " (__e) { ${info.identifier}.$setter = $exp; }));");
  }
}

/** Generates watchers that listen on data changes and update text content. */
class ContentDataBindingEmitter extends DataBindingEmitter<TextInfo> {
  ContentDataBindingEmitter(TextInfo info) : super(info);

  /** Watchers for each data binding. */
  void emitInserted(Context context) {
    var val = info.binding;
    var id = info.identifier;
    var stoppers = context.scope.stoppersName;
    // If possible, watchers update text nodes in place.
    context.insertedMethod.add(
        "$stoppers.add(autogenerated.watchAndInvoke(() => '\${$val}', (__e) {"
        '\n$id = autogenerated.updateBinding($val, $id, __e.newValue);\n}));');
  }
}

/**
 * Emits code for web component instantiation. For example, if the source has:
 *
 *     <x-hello>John</x-hello>
 *
 * And the component has been defined as:
 *
 *    <element name="x-hello" extends="div" constructor="HelloComponent">
 *      <template>Hello, <content>!</template>
 *      <script type="application/dart"></script>
 *    </element>
 *
 * This will ensure that the Dart HelloComponent for `x-hello` is created and
 * attached to the appropriate DOM node.
 */
class ComponentInstanceEmitter extends Emitter<ElementInfo> {
  ComponentInstanceEmitter(ElementInfo info) : super(info);

  void emitCreated(Context context) {
    var component = info.component;
    if (component == null) return;

    var id = info.identifier;
    context.createdMethod.add('new ${component.constructor}.forElement($id)');

    // Note: this feature is deprecated and will be removed.
    info.values.forEach((name, value) {
      context.createdMethod.add('..$name = $value');
    });

    context.createdMethod.add('..created_autogenerated()')
                         .add('..created()')
                         .add('..composeChildren();');
  }

  void emitInserted(Context context) {
    if (info.component == null) return;

    // Note: watchers are intentionally hooked up after inserted() has run,
    // in case it makes any changes to the data.
    var id = info.identifier;
    context.insertedMethod.add('$id.xtag..inserted()')
                          .add('..inserted_autogenerated();');
  }

  void emitRemoved(Context context) {
    if (info.component == null) return;

    var id = info.identifier;
    context.removedMethod.add('$id.xtag..removed_autogenerated()')
                         .add('..removed();');
  }
}

/**
 * Emitter of template conditionals like `<template instantiate="if test">` or
 * `<td template instantiate="if test">`.
 *
 * For a template element, we leave the (childless) template element in the
 * tree and use it as a reference point for child insertion. This matches
 * native MDV behavior.
 *
 * For a template attribute, we leave the (childless) element in the tree as
 * a marker, hidden with 'display:none', and use it as a reference point for
 * insertion.
 */
// TODO(jmesserly): is this good enough for template attributes? we need
// *something* for this case:
// <tr>
//   <td>some stuff</td>
//   <td>other stuff</td>
//   <td template instantiate="if test">maybe this stuff</td>
//   <td template instantiate="if test2">maybe other stuff</td>
//   <td>more random stuff</td>
// </tr>
//
// We can't necessarily rely on child position because of possible mutation,
// unless we're willing to say that "if" requires a fixed number of children.
// If that's the case, we need a way to check for this error case and alert the
// developer.
class ConditionalEmitter extends DataBindingEmitter<TemplateInfo> {
  final _childrenCreated = new CodePrinter();
  final _childrenRemoved = new CodePrinter();
  final _childrenInserted = new CodePrinter();

  ConditionalEmitter(TemplateInfo info) : super(info);

  void emitDeclarations(Context context) {
    super.emitDeclarations(context);
    var id = info.identifier;
    var printer = context.declarations;
    if (info.isTemplateElement) {
      printer.add('autogenerated_html.Node _endPosition$id;');
    }
    printer.add('bool _isVisible$id = false;');
  }

  void emitInserted(Context context) {
    var id = info.identifier;
    var printer = context.insertedMethod;

    var cond = info.ifCondition;
    if (info.isTemplateElement) {
      printer.add('_endPosition$id = $id;');
    }
    var stoppers = context.scope.stoppersName;
    printer.add('''
        $stoppers.add(autogenerated.watchAndInvoke(() => $cond, (__e) {
          bool showNow = __e.newValue;
          if (_isVisible$id && !showNow) {
            _isVisible$id = false;
        ''')
        .add(_childrenRemoved);

    _removeChildNodes(printer);

    printer.add('} else if (!_isVisible$id && showNow) {')
        .add('_isVisible$id = true;')
        .add(_childrenCreated);

    if (info.isTemplateElement) {
      if (info.children.length > 0) {
        var nodes = info.children.map(_createChildExpression);
        nodes[nodes.length - 1] = '_endPosition$id = ${nodes.last}';
        printer.add(
            'autogenerated.insertAllBefore($id.parentNode, $id.nextNode,');
        printer.add('[${Strings.join(nodes, ", ")}]);');
      }
    } else {
      // conditional as attributes mean that the whole conditional is a single
      // node.
      assert(info.children.length == 1);
      var exp = _createChildExpression(info.children[0]);
      printer.add('$id.parentNode.insertBefore($exp, $id.nextNode);');
    }

    printer.add(_childrenInserted).add('''\n}\n}));\n''');
  }

  void emitRemoved(Context context) {
    super.emitRemoved(context);
    var id = info.identifier;
    var printer = context.removedMethod;
    printer.add('if (_isVisible$id) {');
    _removeChildNodes(printer);
    printer.add(_childrenRemoved).add('}');
  }

  /** Adds code to remove all children nodes of the conditional. */
  void _removeChildNodes(CodePrinter printer) {
    var id = info.identifier;
    if (info.isTemplateElement) {
      printer.add(
          '_endPosition$id = autogenerated.removeNodes($id, _endPosition$id);');
    } else {
      printer.add('$id.nextNode.remove();');
    }
  }

  Context contextForChildren(Context c) => new Context(
      c.declarations, _childrenCreated, _childrenInserted, _childrenRemoved,
      new LifecycleScope(c.scope));
}


/**
 * Emitter of template lists like `<template iterate='item in items'>` or
 * `<td template iterate='item in items'>`.
 *
 * For a template element, we leave the (childless) template element in the
 * tree, and use it as a reference point for child insertion. This matches
 * native MDV behavior.
 *
 * For a template attribute, we insert children directly.
 */
class ListEmitter extends DataBindingEmitter<TemplateInfo> {
  final _childrenDeclarations = new CodePrinter();
  final _childrenCreated = new CodePrinter();
  final _childrenRemoved = new CodePrinter();
  final _childrenInserted = new CodePrinter();

  ListEmitter(TemplateInfo info) : super(info);

  String get iterExpr => '${info.loopVariable} in ${info.loopItems}';

  void emitDeclarations(Context context) {
    super.emitDeclarations(context);
    var id = info.identifier;
    var printer = context.declarations;
    printer.add('List<Function> _removeChild$id = [];');
    if (info.isTemplateElement) {
      printer.add('autogenerated_html.Node _endPosition$id;');
    }
  }

  void emitInserted(Context context) {
    var id = info.identifier;
    var items = info.loopItems;
    var printer = context.insertedMethod;

    if (info.isTemplateElement) {
      printer.add('_endPosition$id = $id;');
    }
    var stoppers = context.scope.stoppersName;
    printer.add('''
        $stoppers.add(autogenerated.watchAndInvoke(() => $items, (_) {
          for (var remover in _removeChild$id) remover();
          _removeChild$id.clear();
    ''');

    _removeChildNodes(printer);

    if (info.isTemplateElement) {
      printer.add('var __insert_$id = ${info.identifier}.nextNode;');
    }

    printer.add('for (var $iterExpr) {')
        .add(_childrenDeclarations)
        .add(_childrenCreated);

    if (info.children.length > 0) {
      var nodes = info.children.map(_createChildExpression);
      if (info.isTemplateElement) {
        nodes[nodes.length - 1] = '_endPosition$id = ${nodes.last}';
        printer.add(
            'autogenerated.insertAllBefore($id.parentNode, __insert_$id,');
        printer.add('[${Strings.join(nodes, ", ")}]);');
      } else {
        printer.add('$id.nodes.addAll([${Strings.join(nodes, ", ")}]);');
      }
    }

    printer.add(_childrenInserted)
        .add('_removeChild$id.add(() {')
        .add(_childrenRemoved)
        .add('});\n}\n}));');
  }

  void emitRemoved(Context context) {
    super.emitRemoved(context);
    var id = info.identifier;
    var printer = context.removedMethod;
    _removeChildNodes(printer);
    printer.add('''
        for (var remover in _removeChild$id) remover();
        _removeChild$id.clear();
    ''');
  }

  /** Adds code to remove all children nodes of the loop. */
  void _removeChildNodes(CodePrinter printer) {
    var id = info.identifier;
    if (info.isTemplateElement) {
      printer.add(
          '_endPosition$id = autogenerated.removeNodes($id, _endPosition$id);');
    } else {
      printer.add('$id.nodes.clear();');
    }
  }

  Context contextForChildren(Context c) {
    return new Context(_childrenDeclarations, _childrenCreated,
        _childrenInserted, _childrenRemoved, new LifecycleScope(c.scope));
  }
}


/**
 * An visitor that applies [NodeFieldEmitter], [EventListenerEmitter],
 * [DataBindingEmitter], [DataValueEmitter], [ConditionalEmitter], and
 * [ListEmitter] recursively on a DOM tree.
 */
class RecursiveEmitter extends InfoVisitor {
  final FileInfo _fileInfo;
  Context _context;

  RecursiveEmitter(this._fileInfo, [Context context])
      : _context = context != null ? context : new Context();

  // TODO(jmesserly): currently visiting of components declared in a file is
  // handled separately. Consider refactoring so the base visitor works for us.
  visitFileInfo(FileInfo info) => visit(info.bodyInfo);

  void visitElementInfo(ElementInfo info) {
    if (info.identifier == null) {
      // No need to emit it code for this node.
      super.visitElementInfo(info);
      return;
    }

    // TODO(jmesserly): creating all of these per-element could be expensive.
    // Consider passing info into the emit* methods.
    var fieldEmitter = new ElementFieldEmitter(info);
    var emitters = [fieldEmitter,
        new EventListenerEmitter(info),
        new AttributeEmitter(info),
        new ComponentInstanceEmitter(info)];

    var templateEmitter = null;
    if (info.hasIfCondition) {
      templateEmitter = new ConditionalEmitter(info);
    } else if (info.hasIterate) {
      templateEmitter = new ListEmitter(info);
    }

    var childContext = fieldEmitter.contextForChildren(_context);
    if (templateEmitter != null) {
      emitters.add(templateEmitter);
      childContext = templateEmitter.contextForChildren(_context);
    }

    for (var e in emitters) {
      e.emitDeclarations(_context);
      e.emitCreated(_context);
      e.emitInserted(_context);
    }

    // Remove emitters run in reverse order.
    for (var e in reversed(emitters)) {
      e.emitRemoved(_context);
    }

    var oldContext = _context;
    _context = childContext;

    // Invoke super to visit children.
    super.visitElementInfo(info);

    _context = oldContext;
  }

  void visitTextInfo(TextInfo info) {
    if (info.identifier != null) {
      var emitters =
          [new ContentFieldEmitter(info), new ContentDataBindingEmitter(info)];
      for (var e in emitters) {
        e.emitDeclarations(_context);
        e.emitCreated(_context);
        e.emitInserted(_context);
      }

      for (var e in reversed(emitters)) {
        e.emitRemoved(_context);
      }
    }
    super.visitTextInfo(info);
  }
}

/** Generates the class corresponding to a single web component. */
class WebComponentEmitter extends RecursiveEmitter {
  WebComponentEmitter(FileInfo info) : super(info);

  String run(ComponentInfo info, PathInfo pathInfo) {
    // If this derives from another component, ensure the lifecycle methods are
    // called in the superclass.
    if (info.extendsComponent != null) {
      _context.createdMethod.add('super.created_autogenerated();');
      _context.insertedMethod.add('super.inserted_autogenerated();');
      _context.removedMethod.add('super.removed_autogenerated();');
    }

    _context.createdMethod.add('_root = createShadowRoot();');

    var elemInfo = info.elemInfo;

    // elemInfo is pointing at template tag (no attributes).
    assert(elemInfo.node.tagName == 'element');
    for (var childInfo in elemInfo.children) {
      var node = childInfo.node;
      if (node.tagName == 'template') {
        elemInfo = childInfo;
        break;
      }
    }

    if (info.element.attributes['apply-author-styles'] != null) {
      _context.createdMethod.add('if (_root is autogenerated_html.ShadowRoot) '
          '_root.applyAuthorStyles = true;');
      // TODO(jmesserly): warn at runtime if apply-author-styles was not set,
      // and we don't have Shadow DOM support? In that case, styles won't have
      // proper encapsulation.
    }
    if (info.template != null && !elemInfo.childrenCreatedInCode) {
      // TODO(jmesserly): we need to emit code to run the <content> distribution
      // algorithm for browsers without ShadowRoot support.
      _context.createdMethod.add("_root.innerHtml = '''")
          .addRaw(escapeDartString(elemInfo.node.innerHTML, triple: true))
          .addRaw("''';\n");
    }

    visit(elemInfo);

    bool hasExtends = info.extendsComponent != null;
    var codeInfo = info.userCode;
    if (codeInfo == null) {
      var superclass = hasExtends ? info.extendsComponent.constructor
          : 'autogenerated.WebComponent';
      codeInfo = new DartCodeInfo(null, null, [],
          'class ${info.constructor} extends $superclass {\n}');
    }

    var code = codeInfo.code;
    var match = new RegExp('class ${info.constructor}[^{]*{').firstMatch(code);
    if (match != null) {
      var printer = new CodePrinter();
      var libraryName = (codeInfo.libraryName != null)
          ? codeInfo.libraryName
          : info.tagName.replaceAll(new RegExp('[-./]'), '_');
      printer.add(codegen.header(info.declaringFile.path, libraryName));

      // Add exisitng import, export, and part directives.
      for (var directive in codeInfo.directives) {
        printer.add(codegen.directiveText(directive, info, pathInfo));
      }

      // Add imports only for those components used by this component.
      var imports = info.usedComponents.keys.map(
          (c) => pathInfo.relativePath(info, c));

      if (hasExtends) {
        // Inject an import to the base component.
        printer.add(codegen.importList(
            [pathInfo.relativePath(info, info.extendsComponent)]));
      }

      printer.add(codegen.importList(imports))
          .add(code.substring(0, match.end))
          .add('\n')
          .add(codegen.componentCode(info.constructor,
              _context.declarations.formatString(1),
              _context.createdMethod.formatString(2),
              _context.insertedMethod.formatString(2),
              _context.removedMethod.formatString(2)))
          .add(code.substring(match.end));
      return printer.formatString();
    } else {
      _context.messages.error('please provide a class definition '
          'for ${info.constructor}:\n $code', info.element.sourceSpan,
          file: info.inputPath);
      return '';
    }
  }
}

/** Generates the class corresponding to the main html page. */
class MainPageEmitter extends RecursiveEmitter {
  MainPageEmitter(FileInfo fileInfo) : super(fileInfo);

  String run(Document document, PathInfo pathInfo) {
    visit(_fileInfo.bodyInfo);

    // fix up the URLs to content that is not modified by the compiler
    document.queryAll('script').forEach((tag) {
    var src = tag.attributes["src"];
     if (tag.attributes['type'] == 'application/dart') {
       tag.remove();
     } else if (src != null) {
       tag.attributes["src"] = pathInfo.transformUrl(_fileInfo.path, src);
     }
    });
    document.queryAll('link').forEach((tag) {
     var href = tag.attributes['href'];
       if (tag.attributes['rel'] == 'components') {
         tag.remove();
       } else if (href != null) {
         tag.attributes['href'] = pathInfo.transformUrl(_fileInfo.path, href);
       }
     });

    var printer = new CodePrinter();

    // Inject library name if not pressent.
    var codeInfo = _fileInfo.userCode;
    var libraryName = codeInfo.libraryName != null
        ? codeInfo.libraryName : _fileInfo.libraryName;
    printer.add(codegen.header(_fileInfo.path, libraryName));

    // Add exisitng import, export, and part directives.
    for (var directive in codeInfo.directives) {
      printer.add(codegen.directiveText(directive, _fileInfo, pathInfo));
    }

    // Import only those components used by the page.
    var imports = _fileInfo.usedComponents.keys.map(
          (c) => pathInfo.relativePath(_fileInfo, c));
    printer.add(codegen.importList(imports))
        .addRaw(codegen.mainDartCode(codeInfo.code,
            _context.declarations.formatString(1),
            _context.createdMethod.formatString(1),
            _context.insertedMethod.formatString(1)));
    return printer.formatString();
  }
}

String _createChildExpression(NodeInfo info) {
  if (info.identifier != null) return info.identifier;
  return _emitCreateHtml(info.node);
}

/**
 * An (runtime) expression to create the [node]. It always includes the node's
 * attributes, but only includes children nodes if [includeChildren] is true.
 */
String _emitCreateHtml(Node node) {
  if (node is Text) {
    return "new autogenerated_html.Text('${escapeDartString(node.value)}')";
  }

  // Namespace constants from:
  // http://dev.w3.org/html5/spec/namespaces.html#namespaces
  var isHtml = node.namespace == 'http://www.w3.org/1999/xhtml';
  var isSvg = node.namespace == 'http://www.w3.org/2000/svg';
  var isEmpty = node.attributes.length == 0 && node.nodes.length == 0;

  var constructor;
  // Generate precise types like "new ButtonElement()" if we can.
  if (isEmpty && isHtml) {
    constructor = htmlElementConstructors[node.tagName];
    if (constructor != null) {
      constructor = '$constructor()';
    } else {
      constructor = "html.Element.tag('${node.tagName}')";
    }
  } else if (isEmpty && isSvg) {
    constructor = "svg.Element.tag('${node.tagName}')";
  } else {
    // TODO(sigmund): does this work for the mathml namespace?
    var target = isSvg ? 'svg.SvgElement.svg' : 'html.Element.html';
    constructor = "$target('${escapeDartString(node.outerHTML)}')";
  }
  return 'new autogenerated_$constructor';
}

/**
 * Finds the correct expression to set an HTML attribute through the DOM.
 * It is important for correctness to use the DOM setter if it is available.
 * Otherwise changes will not be applied. This is most easily observed with
 * "InputElement.value", ".checked", etc.
 */
String _findDomField(ElementInfo info, String name) {
  var typeName = typeForHtmlTag(info.baseTagName);
  while (typeName != null) {
    var fields = htmlElementFields[typeName];
    if (fields != null) {
      var field = fields[name];
      if (field != null) return field;
    }
    typeName = htmlElementExtends[typeName];
  }
  // If we didn't find a DOM setter, and this is a component, set a property on
  // the component.
  if (info.component != null && !name.startsWith('data-')) {
    return 'xtag.${toCamelCase(name)}';
  }
  return "attributes['$name']";
}
