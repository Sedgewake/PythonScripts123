shader_type sky;

render_mode skip_fog; // We handle fog manually

uniform vec3 top_color : source_color;       // North Pole
uniform vec3 middle_color : source_color;    // Equator
uniform vec3 bottom_color : source_color;    // South Pole
uniform vec3 sun_color : source_color;       // Sun highlight

uniform sampler2D cloud_tex : hint_albedo;
uniform float speed = 0.5;
uniform float alpha = 0.985;
uniform float exposure = 1.0;
uniform float fog_level = 0.5;

void fragment() {
    // Sky direction
    vec3 dir = normalize(SKY_COORDS);

    // Horizon gradient blend
    float y = dir.y;
    float t1 = max(y, 0.0);   // upward blend
    float t2 = max(-y, 0.0);  // downward blend
    vec3 gradient = mix(mix(middle_color, top_color, t1), bottom_color, t2);

    // Time for cloud scrolling
    float t = TIME * speed;

    // UV projection from spherical to flattened dome
    vec3 pos = normalize(SKY_COORDS);
    float uv1 = pow(dot(vec4(0.0, 5.0, 0.0, -1.0), vec4(pos, 10.0)), 3.0);
    vec2 uv = pos.xz * uv1 * 0.001;

    // Two scrolling cloud layers
    vec3 cloud1 = texture(cloud_tex, uv + vec2(t * 0.01, t * 0.02)).rgb;
    vec3 cloud2 = texture(cloud_tex, uv * 1.7 + vec2(t * 0.03, t * 0.05)).rgb;
    vec3 clouds = 1.0 - ((1.0 - cloud1 * cloud2) * alpha);

    // Sun highlight
    vec3 sun_dir = normalize(DIRECTIONAL_LIGHT.direction);
    float sun_strength = pow((dot(dir, sun_dir) + 1.0) * 0.5, 20.0);
    vec3 sun = sun_color * sun_strength;

    // Combine
    vec3 color = (gradient + sun) * clouds;

    // Fog near horizon
    float fog_factor = clamp(1.0 - y, 0.0, 1.0) * fog_level;
    color = mix(color, FOG_COLOR.rgb, fog_factor);

    COLOR = vec4(color * exposure, 1.0);
}
