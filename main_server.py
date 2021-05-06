import argparse
import configparser
import subprocess
import json
import os

# Read Configuration
config = configparser.ConfigParser()
if os.path.isfile('config.ini'):
    config.read('config.ini')
else:
    print('missing config.ini')
    quit()

# Read settings, create defaults if missing
default_jsons = {}
if os.path.isfile('settings.json'):
    with open('settings.json') as json_file:
        default_jsons = json.load(json_file)

else:
    default_jsons['settings'] = []

    default_jsons['settings'].append({'resolution': '1024', 'dilation_width': 32.0, 'apply_diffusion': False, 'max_frontal': 0.01, 'max_rear': 0.01, 'max_dist_relative_scale': True, 'average_normals': True, 'ignore_backface': True, 'antialiasing': 'Subsampling 4x4', 'match': 'Always', 'name_suffix_low': '_low', 'name_suffix_high': '_high', 'name_suffix_ignore_backface': '_ignorebf', 'secondary_rays': 64.0, 'min_occluder_distance': 0.0001, 'max_occluder_distance': 1.0, 'relative_to_bbox': True, 'spread_angle': 180.0, 'ray_distrib': 'Cosine', 'ignore_backface_secondary': 'Never', 'self_occlusion': 'Only Same Mesh Name', 'attenuation': 'Linear', 'enable_ground_plane': True, 'ground_offset': '0', 'output_format': 'jpg'})

    with open('settings.json', 'w') as outfile:
        json.dump(default_jsons, outfile, indent=4)

# Main function
def main(folder, settings):

    if folder:
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith(('.fbx')):

                    file_path = os.path.join(root, filename)

                    # Gather info on the object
                    args = str(config['locations']['sub_auto_tool'])
                    args += str("sbsbaker.exe info --hide-location --hide-bounding-box ") # File
                    args += '"' + str(file_path) + '"' # Mesh files to process. This option is implicit, so you can just provide a list of files at the end of your arguments, they will be interpreted as inputs.

                    temp = subprocess.Popen(args, stdout = subprocess.PIPE)

                    # we use the communicate function to fetch the output
                    output = str(temp.communicate())

                    # splitting the output so that we can parse them line by line
                    output = output.split("\\r\\n")

                    # a variable to store the output
                    res = []

                    # iterate through the output line by line
                    for line in output:
                        if line.find('Entity') != -1:
                            clean_line = line.replace('  Entity "', '').replace('":', '')
                            res.append(clean_line)
                            # print(' Found: ' + clean_line)

                    for node in res:
                        # General parameters
                        args = str(config['locations']['sub_auto_tool'])
                        args += str("sbsbaker.exe ambient-occlusion-from-mesh") # File
                        args += ' --inputs "' + str(file_path) +'"' # Mesh files to process. This option is implicit, so you can just provide a list of files at the end of your arguments, they will be interpreted as inputs.

                        resolutions = {
                            "512": 9,
                            "1024": 10,
                            "2048": 11,
                            "4096": 12,
                        }
                        resolution = resolutions.get(settings['resolution'], 11)
                        args += ' --output-size ' + str(resolution) + ',' + str(resolution) # Output size of the generated map.<w> and <h> are the exponents of powers of 2 that give the actual width and height.

                        args += ' --dilation-width ' + str(int(settings['dilation_width'])) # Width of the dilation post-process (in pixels) applied before diffusion.
                        args += ' --apply-diffusion ' + str(settings['apply_diffusion']).lower() # Whether to use diffusion as a post-process after dilation, or not.
                        args += ' --max-frontal ' + str(settings['max_frontal']) # Max frontal distance for raytracing.
                        args += ' --max-rear ' + str(settings['max_rear']) # Max rear distance for raytracing.
                        args += ' --max-dist-relative-scale ' + str(settings['max_dist_relative_scale']).lower() # Interpret the Occluder Distance as a factor of the mesh bounding box.
                        args += ' --average-normals ' + str(settings['average_normals']).lower() # Interpret the Occluder Distance as a factor of the mesh bounding box.
                        args += ' --ignore-backface ' + str(settings['ignore_backface']).lower() # Interpret the Occluder Distance as a factor of the mesh bounding box.

                        antialiasings = {
                            'None': 0,
                            'Subsampling 2x2': 1,
                            'Subsampling 4x4': 2,
                            'Subsampling 8x8': 3,
                        }
                        antialiasing = antialiasings.get(settings['antialiasing'], 0)
                        args += ' --antialiasing ' + str(antialiasing) # Antialiasing method.

                        match = {
                            'Always': 0,
                            'By Mesh Name': 1,
                        }
                        match = match.get(settings['match'], 0)
                        args += ' --match ' + str(match) # Antialiasing method.

                        args += ' --name-suffix-low ' + str(settings['name_suffix_low']) # Low Poly name suffix.
                        args += ' --name-suffix-high ' + str(settings['name_suffix_high']) # High Poly name suffix.

                        # Ambient Occlusion Parameters
                        args += ' --nb-second-rays ' + str(int(settings['secondary_rays'])) # Number of secondary rays (in [1; 256]).
                        args += ' --min-dist ' + str(settings['min_occluder_distance']) # Minimum Occluder Distance (bias).
                        args += ' --max-rear ' + str(settings['max_occluder_distance']) # Minimum Occluder Distance (bias).
                        args += ' --relative-to-bbox ' + str(settings['relative_to_bbox']).lower() # Interpret the max distances as a factor of the mesh bounding box.
                        args += ' --spread-angle ' + str(settings['spread_angle']) # Maximum spread angle of occlusion rays.

                        ray_distrib = {
                            'Uniform': 0,
                            'Cosine': 1,
                        }
                        ray_distrib = ray_distrib.get(settings['ray_distrib'], 0)
                        args += ' --ray-distrib ' + str(ray_distrib) # Angular Distribution of Occlusion Rays. (0='Uniform', 1='Cosine')

                        ignore_backface_secondary = {
                            'Never': 0,
                            'Always': 1,
                            'By Mesh Name': 2,
                        }
                        ignore_backface_secondary = ignore_backface_secondary.get(settings['ignore_backface_secondary'], 0)
                        args += ' --ignore-backface-secondary ' + str(ignore_backface_secondary) # Angular Distribution of Occlusion Rays. (0='Uniform', 1='Cosine')

                        self_occlusion = {
                            'Always': 0,
                            'Only Same Mesh Name': 1,
                        }
                        self_occlusion = self_occlusion.get(settings['self_occlusion'], 0)
                        args += ' --self-occlusion ' + str(self_occlusion) # Choose what geometry will cause occlusion. (0='Always', 1='Only Same Mesh Name')

                        attenuation = {
                            'None': 0,
                            'Smooth': 1,
                            'Linear': 2,
                        }
                        attenuation = attenuation.get(settings['attenuation'], 0)
                        args += ' --ignore-backface-secondary ' + str(attenuation) # How occlusion is attenuated by occluder distance (0='None', 1='Smooth', 2='Linear')

                        args += ' --enable-ground-plane ' + str(settings['enable_ground_plane']).lower() # If enabled, adds an infinite plane under the baked mesh.
                        args += ' --ground-offset ' + str(settings['ground_offset']) # Offset of the ground plane from the mesh lowest point.

                        # Misc
                        args += ' --use-lowdef-as-highdef true' # Skip scene request

                        # --Output
                        args += ' --output-name mat_' + node + '_ambient_occlusion' # Nodename
                        args += ' --input-selection ' + node # Nodename
                        args += ' --output-format ' + str(settings['output_format']) # Format to use for output image file.

                        # Set output path
                        output_path = os.path.join(file_path, '../ao_gen')

                        if not os.path.exists(output_path):
                            os.makedirs(output_path)
                        args += ' --output-path "' + str(output_path) + '"'# Set the output path for the generated files. By default the output path is the current directory.

                        print('Processing ' + node)

                        # print(args)
                        rendering = subprocess.Popen(args)

                        rendering.wait() # Hold on till process is finished

                        print('- Exported ' + node)

    else:
        print('Please select a valid folder')

if __name__ == '__main__':

    # Initialize
    parser = argparse.ArgumentParser(description='Process some moddels.')
    parser.add_argument('-f', '--folder', help='Source models folder', required=True)

    args = parser.parse_args()

    # Get defaults
    settings = default_jsons["settings"][0]

    try:
        main(args.folder, settings)
    except KeyboardInterrupt:
        print('Ended!')
