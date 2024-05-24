#include <math.h>
#include <stdint.h>
#include <stdlib.h>

//COMPILE WITH:
// gcc -shared -o raycasting.so -fPIC raycast.c -lm

// LIMITED EDITION

// void ray_casting(uint8_t *screen_array, float *player_pos, double player_angle, double player_height,
//                  double player_pitch, int screen_width, int screen_height, double delta_angle,
//                  int ray_distance, double h_fov, double scale_height, uint8_t *height_map,
//                  uint8_t *color_map, int map_width, int map_height) {

//     for (int i = 0; i < screen_width * screen_height; i++) {
//         screen_array[i * 3] = 119;     // R
//         screen_array[i * 3 + 1] = 241; // G
//         screen_array[i * 3 + 2] = 255; // B
//     }

//     int *y_buffer = (int*)malloc(screen_width * sizeof(int));
//     for (int i = 0; i < screen_width; i++) {
//         y_buffer[i] = screen_height;
//     }

//     double *ray_angles = (double*)malloc(screen_width * sizeof(double));
//     double *sin_a = (double*)malloc(screen_width * sizeof(double));
//     double *cos_a = (double*)malloc(screen_width * sizeof(double));

//     for (int i = 0; i < screen_width; i++) {
//         ray_angles[i] = player_angle - h_fov + delta_angle * i;
//         sin_a[i] = sin(ray_angles[i]);
//         cos_a[i] = cos(ray_angles[i]);
//     }

//     for (int num_ray = 0; num_ray < screen_width; num_ray++) {
//         int first_contact = 0;
//         for (int depth = 1; depth < ray_distance; depth++) {
//             int x = (int)(player_pos[0] + depth * cos_a[num_ray]);
//             int y = (int)(player_pos[1] + depth * sin_a[num_ray]);

//             if (0 < x && x < map_width && 0 < y && y < map_height) {
//                 double depth_corrected = depth * cos(player_angle - ray_angles[num_ray]);
//                 int height_on_screen = (int)((player_height - height_map[x * map_height + y]) / depth_corrected * scale_height + player_pitch);

//                 if (!first_contact) {
//                     y_buffer[num_ray] = height_on_screen < screen_height ? height_on_screen : screen_height;
//                     first_contact = 1;
//                 }

//                 if (height_on_screen < 0) {
//                     height_on_screen = 0;
//                 }

//                 if (height_on_screen < y_buffer[num_ray]) {
//                     for (int screen_y = height_on_screen; screen_y < y_buffer[num_ray]; screen_y++) {
//                         int idx = (num_ray * screen_height + screen_y) * 3;
//                         screen_array[idx] = color_map[(x * map_height + y) * 3];
//                         screen_array[idx + 1] = color_map[(x * map_height + y) * 3 + 1];
//                         screen_array[idx + 2] = color_map[(x * map_height + y) * 3 + 2];
//                     }
//                     y_buffer[num_ray] = height_on_screen;
//                 }
//             }
//         }
//     }

//     free(y_buffer);
//     free(ray_angles);
//     free(sin_a);
//     free(cos_a);
// }


// ENDLESS EDITION
void ray_casting(uint8_t *screen_array, float *player_pos, double player_angle, double player_height,
                 double player_pitch, int screen_width, int screen_height, double delta_angle,
                 int ray_distance, double h_fov, double scale_height, uint8_t *height_map,
                 uint8_t *color_map, int map_width, int map_height) {

    for (int i = 0; i < screen_width * screen_height; i++) {
        screen_array[i * 3] = 119;     // R
        screen_array[i * 3 + 1] = 241; // G
        screen_array[i * 3 + 2] = 255; // B
    }

    int *y_buffer = (int*)malloc(screen_width * sizeof(int));
    for (int i = 0; i < screen_width; i++) {
        y_buffer[i] = screen_height;
    }

    double *ray_angles = (double*)malloc(screen_width * sizeof(double));
    double *sin_a = (double*)malloc(screen_width * sizeof(double));
    double *cos_a = (double*)malloc(screen_width * sizeof(double));

    for (int i = 0; i < screen_width; i++) {
        ray_angles[i] = player_angle - h_fov + delta_angle * i;
        sin_a[i] = sin(ray_angles[i]);
        cos_a[i] = cos(ray_angles[i]);
    }

    for (int num_ray = 0; num_ray < screen_width; num_ray++) {
        int first_contact = 0;
        for (int depth = 1; depth < ray_distance; depth++) {
            int x = (int)(player_pos[0] + depth * cos_a[num_ray]) % map_width;
            int y = (int)(player_pos[1] + depth * sin_a[num_ray]) % map_height;

            // Ensure non-negative indices
            if (x < 0) x += map_width;
            if (y < 0) y += map_height;

            if (0 <= x && x < map_width && 0 <= y && y < map_height) {
                double depth_corrected = depth * cos(player_angle - ray_angles[num_ray]);
                int height_on_screen = (int)((player_height - height_map[x * map_height + y]) / depth_corrected * scale_height + player_pitch);

                if (!first_contact) {
                    y_buffer[num_ray] = height_on_screen < screen_height ? height_on_screen : screen_height;
                    first_contact = 1;
                }

                if (height_on_screen < 0) {
                    height_on_screen = 0;
                }

                if (height_on_screen < y_buffer[num_ray]) {
                    for (int screen_y = height_on_screen; screen_y < y_buffer[num_ray]; screen_y++) {
                        int idx = (num_ray * screen_height + screen_y) * 3;
                        screen_array[idx] = color_map[(x * map_height + y) * 3];
                        screen_array[idx + 1] = color_map[(x * map_height + y) * 3 + 1];
                        screen_array[idx + 2] = color_map[(x * map_height + y) * 3 + 2];
                    }
                    y_buffer[num_ray] = height_on_screen;
                }
            }
        }
    }

    free(y_buffer);
    free(ray_angles);
    free(sin_a);
    free(cos_a);
}