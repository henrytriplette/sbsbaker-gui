import PySimpleGUI as sg
import configparser
import subprocess
import os

# Read Configuration
config = configparser.ConfigParser()
config.read('config.ini')

def main():

    sg.theme('Topanga')

    main_panel = [
        [sg.Text('Input Folder', size=(15, 1)), sg.Input(key='inputMainPanelMeshFolder'), sg.FolderBrowse(target=('inputMainPanelMeshFolder'))],

        [sg.Text('Output Path', size=(15, 1)), sg.Input(default_text="/", key='output_path'), sg.FolderBrowse(target=('output_path'))],

        [sg.Text('Output format', size=(55, 1)),
         sg.Combo(['surface', 'dds', 'bmp', 'jpg', 'jif', 'jpeg', 'jpe', 'png', 'tga', 'targa', 'tif', 'tiff', 'wap', 'wbmp', 'wbm', 'psd', 'psb', 'hdr', 'exr', 'webp'], default_value='jpg', size=(15, 1), key="output_format")],

        # Common Parameters
        [sg.Text('                  ', size=(55, 2))],
        [sg.Text('Common Parameters.', size=(55, 1))],

        [sg.Text('Output Size', size=(55, 1)),
         sg.Combo(['512', '1024', '2048', '4096'], default_value='1024', size=(15, 1), key="resolution")],

        [sg.Text('Dilation Width', size=(55, 1)),
         sg.Slider(range=(1,100), default_value=32, size=(20,15), orientation='horizontal', key="dilation_width")], # INTEGER

        [sg.Text('Apply Diffusion', size=(55, 1)),
         sg.Checkbox('Apply Diffusion', default=False, size=(15, 1), key="apply_diffusion")],

        [sg.Text('Max Frontal Distance', size=(55, 1)),
         sg.Slider(range=(0.00,1.00), resolution=0.01, default_value=0.01, size=(20,15), orientation='horizontal', key="max_frontal")], # INTEGER

        [sg.Text('Max Rear Distance', size=(55, 1)),
         sg.Slider(range=(0.00,1.00), resolution=0.01, default_value=0.01, size=(20,15), orientation='horizontal', key="max_rear")], # INTEGER

        [sg.Text('Relative to Bounding Box', size=(55, 1)),
         sg.Checkbox('Relative to Bounding Box', default=True, size=(15, 1), key="max_dist_relative_scale")],

        [sg.Text('Average Normals', size=(55, 1)),
         sg.Checkbox('Average Normals', default=True, size=(15, 1), key="average_normals")],

        [sg.Text('Ignore Backface', size=(55, 1)),
         sg.Checkbox('Ignore Backface', default=True, size=(15, 1), key="ignore_backface")],

        [sg.Text('Antialiasing method.', size=(55, 1)),
         sg.Combo(['None', 'Subsampling 2x2', 'Subsampling 4x4', 'Subsampling 8x8'], default_value='Subsampling 4x4', size=(15, 1), key="antialiasing")],

        [sg.Text('Match.', size=(55, 1)),
         sg.Combo(['Always', 'By Mesh Name'], default_value='Always', size=(15, 1), key="match")],

        [sg.Text('Low Poly name suffix.', size=(55, 1)),
         sg.Input(default_text = "_low", size=(20,15), key="name_suffix_low")], # STRING

        [sg.Text('High Poly name suffix', size=(55, 1)),
         sg.Input(default_text = "_high", size=(20,15), key="name_suffix_high")], # STRING

        [sg.Text('Ignore backface suffix', size=(55, 1)),
         sg.Input(default_text = "_ignorebf", size=(20,15), key="name_suffix_ignore_backface")], # STRING

         # ambient-occlusion options
        [sg.Text('                  ', size=(55, 2))],
        [sg.Text('# Ambient occlusion options.', size=(55, 2))],

        [sg.Text('Secondary Rays', size=(55, 1)),
         sg.Slider(range=(1,256), resolution=1, default_value=64, size=(20,15), orientation='horizontal', key="secondary_rays")], # INTEGER

        [sg.Text('Min Occluder Distance', size=(55, 1)),
         sg.Slider(range=(0.00,1.00), resolution=0.0001, default_value=0.0001, size=(20,15), orientation='horizontal', key="min_occluder_distance")], # INTEGER

        [sg.Text('Max Occluder Distance', size=(55, 1)),
         sg.Slider(range=(0.00,1.00), resolution=0.01, default_value=1, size=(20,15), orientation='horizontal', key="max_occluder_distance")], # INTEGER

        [sg.Text('Relative to Bounding Box', size=(55, 1)),
         sg.Checkbox('Relative to Bounding Box', default=True, size=(15, 1), key="relative_to_bbox")],

        [sg.Text('Spread angle', size=(55, 1)),
         sg.Slider(range=(0,256), resolution=1, default_value=180, size=(20,15), orientation='horizontal', key="spread_angle")], # INTEGER

        [sg.Text('Angular Distribution of Occlusion Rays.', size=(55, 1)),
         sg.Combo(['Uniform', 'Cosine'], default_value='Cosine', size=(15, 1), key="ray_distrib")],

        [sg.Text('Ignore Backface.', size=(55, 1)),
         sg.Combo(['Never', 'Always', 'By Mesh Name'], default_value='Never', size=(15, 1), key="ignore_backface_secondary")],

        [sg.Text('Self Occlusion.', size=(55, 1)),
         sg.Combo(['Always', 'Only Same Mesh Name'], default_value='Only Same Mesh Name', size=(15, 1), key="self_occlusion")],

        [sg.Text('Attenuation.', size=(55, 1)),
         sg.Combo(['None', 'Smooth', 'Linear'], default_value='Linear', size=(15, 1), key="attenuation")],

        [sg.Text('Ground Plane', size=(55, 1)),
         sg.Checkbox('Enable Floor', default=True, size=(15, 1), key="enable_ground_plane")],

        [sg.Text('Ground Plane Offset.', size=(55, 1)),
         sg.Input(default_text = "0", size=(20,15), key="ground_offset")], # STRING

        # Buttons
        [sg.Text('                  ', size=(55, 2))],
        [sg.Button('Start processing folder', size=(25, 1), key='utility_RunSbsbaker')],

    ]

    layout = [
                [sg.TabGroup(
                    [
                        [
                        sg.Tab('Sbsbaker Utility', main_panel, tooltip='Sbsbaker Utility'),
                        ]
                    ])
                ],
                [sg.Cancel(key='quit')],
            ]

    window = sg.Window('Sbsbaker Utility - 0.12 Alpha', layout)

    # Processes
    processes = []

    while (True):

        # This is the code that reads and updates your window
        event, values = window.Read(timeout=100)

        if event == 'Exit' or event is None:
            break

        if event == 'quit':
            break

        # Vpype Flow Imager
        if event == 'utility_RunSbsbaker':
            if values['inputMainPanelMeshFolder']:

                for root, dirs, files in os.walk(values['inputMainPanelMeshFolder']):
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
                                    sg.Print(' Found: ' + clean_line)

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
                                resolution = resolutions.get(values['resolution'], 11)
                                args += ' --output-size ' + str(resolution) + ',' + str(resolution) # Output size of the generated map.<w> and <h> are the exponents of powers of 2 that give the actual width and height.

                                args += ' --dilation-width ' + str(int(values['dilation_width'])) # Width of the dilation post-process (in pixels) applied before diffusion.
                                args += ' --apply-diffusion ' + str(values['apply_diffusion']).lower() # Whether to use diffusion as a post-process after dilation, or not.
                                args += ' --max-frontal ' + str(values['max_frontal']) # Max frontal distance for raytracing.
                                args += ' --max-rear ' + str(values['max_rear']) # Max rear distance for raytracing.
                                args += ' --max-dist-relative-scale ' + str(values['max_dist_relative_scale']).lower() # Interpret the Occluder Distance as a factor of the mesh bounding box.
                                args += ' --average-normals ' + str(values['average_normals']).lower() # Interpret the Occluder Distance as a factor of the mesh bounding box.
                                args += ' --ignore-backface ' + str(values['ignore_backface']).lower() # Interpret the Occluder Distance as a factor of the mesh bounding box.

                                antialiasings = {
                                    'None': 0,
                                    'Subsampling 2x2': 1,
                                    'Subsampling 4x4': 2,
                                    'Subsampling 8x8': 3,
                                }
                                antialiasing = antialiasings.get(values['antialiasing'], 0)
                                args += ' --antialiasing ' + str(antialiasing) # Antialiasing method.

                                match = {
                                    'Always': 0,
                                    'By Mesh Name': 1,
                                }
                                match = match.get(values['match'], 0)
                                args += ' --match ' + str(match) # Antialiasing method.

                                args += ' --name-suffix-low ' + str(values['name_suffix_low']) # Low Poly name suffix.
                                args += ' --name-suffix-high ' + str(values['name_suffix_high']) # High Poly name suffix.

                                # Ambient Occlusion Parameters
                                args += ' --nb-second-rays ' + str(int(values['secondary_rays'])) # Number of secondary rays (in [1; 256]).
                                args += ' --min-dist ' + str(values['min_occluder_distance']) # Minimum Occluder Distance (bias).
                                args += ' --max-rear ' + str(values['max_occluder_distance']) # Minimum Occluder Distance (bias).
                                args += ' --relative-to-bbox ' + str(values['relative_to_bbox']).lower() # Interpret the max distances as a factor of the mesh bounding box.
                                args += ' --spread-angle ' + str(values['spread_angle']) # Maximum spread angle of occlusion rays.

                                ray_distrib = {
                                    'Uniform': 0,
                                    'Cosine': 1,
                                }
                                ray_distrib = ray_distrib.get(values['ray_distrib'], 0)
                                args += ' --ray-distrib ' + str(ray_distrib) # Angular Distribution of Occlusion Rays. (0='Uniform', 1='Cosine')

                                ignore_backface_secondary = {
                                    'Never': 0,
                                    'Always': 1,
                                    'By Mesh Name': 2,
                                }
                                ignore_backface_secondary = ignore_backface_secondary.get(values['ignore_backface_secondary'], 0)
                                args += ' --ignore-backface-secondary ' + str(ignore_backface_secondary) # Angular Distribution of Occlusion Rays. (0='Uniform', 1='Cosine')

                                self_occlusion = {
                                    'Always': 0,
                                    'Only Same Mesh Name': 1,
                                }
                                self_occlusion = self_occlusion.get(values['self_occlusion'], 0)
                                args += ' --self-occlusion ' + str(self_occlusion) # Choose what geometry will cause occlusion. (0='Always', 1='Only Same Mesh Name')

                                attenuation = {
                                    'None': 0,
                                    'Smooth': 1,
                                    'Linear': 2,
                                }
                                attenuation = attenuation.get(values['attenuation'], 0)
                                args += ' --ignore-backface-secondary ' + str(attenuation) # How occlusion is attenuated by occluder distance (0='None', 1='Smooth', 2='Linear')

                                args += ' --enable-ground-plane ' + str(values['enable_ground_plane']).lower() # If enabled, adds an infinite plane under the baked mesh.
                                args += ' --ground-offset ' + str(values['ground_offset']) # Offset of the ground plane from the mesh lowest point.

                                # Misc
                                args += ' --use-lowdef-as-highdef true' # Skip scene request

                                # --Output
                                args += ' --output-name mat_' + node + '_ambient_occlusion' # Nodename
                                args += ' --input-selection ' + node # Nodename
                                args += ' --output-format ' + str(values['output_format']) # Format to use for output image file.

                                output_path = values['output_path'];
                                if (output_path == '/'):
                                    output_path = os.path.join(file_path, '..')
                                args += ' --output-path "' + str(output_path) + '"'# Set the output path for the generated files. By default the output path is the current directory.

                                sg.Print('Processing ' + node)

                                # print(args)
                                rendering = subprocess.Popen(args)
                                processes.append(rendering) # Append process to queque

                                rendering.wait() # Hold on till process is finished

                                sg.Print('- Exported ' + node)

            else:
                sg.popup_error('Please select a valid folder')

            sg.Print('Done Exporting')

    window.Close()   # Don't forget to close your window!

    # Kill all processes
    for process in processes:
        process.kill()

if __name__ == '__main__':
    main()
