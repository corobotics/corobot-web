// Light color
uniform vec4 lightColor;

// Diffuse reflection color
uniform vec4 diffuseColor;

uniform vec4 specColor;

uniform float exponent;

// Vectors "attached" to vertex and get sent to fragment shader
varying vec3 lPos;
varying vec3 vPos;
varying vec3 vNorm;


void main()
{        
    // calculate your vectors
    vec3 L = normalize (lPos - vPos);
    vec3 N = normalize (vNorm);
    vec3 R=normalize(reflect(-L,N));
    vec3 E = normalize(-vPos);
    vec4 currcolor=lightColor * diffuseColor * (dot(N, L));
    vec4 specAdd=lightColor*specColor* pow( dot(R,E),exponent );
    currcolor=specAdd+currcolor;
    // set the final color
    gl_FragColor = currcolor;

}
