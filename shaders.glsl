
---VERTEX SHADER---

uniform mat4 projection_mat;
uniform mat4 modelview_mat;
attribute vec3 v_pos;
attribute vec3 color;

varying vec3 frag_color;

void main(void){
    gl_Position = projection_mat * modelview_mat * vec4(v_pos, 1.0);
    frag_color = color;
}

---FRAGMENT SHADER---

varying vec3 frag_color;

void main(void){
    gl_FragColor = vec4(frag_color,1.0);
}



