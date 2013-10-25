// Copyright (c) 2012, the Dart project authors.  Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

library files;

import 'package:html5lib/dom.dart';
import 'file_system/path.dart';
import 'info.dart';

/** An input file to process by the template compiler. */
class SourceFile {
  final Path path;

  final bool isDart;
  Document document;
  String code;

  SourceFile(this.path, {this.isDart: false});

  String toString() => "<#SourceFile $path>";
}

/** An output file to generated by the template compiler. */
class OutputFile {
  final Path path;
  final String contents;
  
  /** 
   * Path to the source file that was transformed into this OutputFile, `null`
   * for files that are generated and do not correspond to an input
   * [SourceFile].
   */
  final Path source;

  OutputFile(this.path, this.contents, {Path source})
      : source = source;
}
