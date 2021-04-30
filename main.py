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

        # Common Parameters
        [sg.Text('Common Parameters.', size=(55, 1))],

        [sg.Text('Output Size', size=(55, 1)),
         sg.Combo(['512', '1024', '2048', '4096'], default_value='1024', size=(15, 1), key="resolution")],

        [sg.Text('Dilation Width', size=(55, 1)),
         sg.Slider(range=(1,100), default_value=32, size=(20,15), orientation='horizontal', key="dilation_width")], # INTEGER

        [sg.Text('Apply Diffusion', size=(55, 1)),
         sg.Checkbox('Apply Diffusion', default=False, size=(15, 1), key="apply_diffusion")],

        [sg.Text('Max Frontal Distance', size=(55, 1)),
         sg.Slider(range=(0,1), default_value=0.01, size=(20,15), orientation='horizontal', key="max_frontal")], # INTEGER

        [sg.Text('Max Rear Distance', size=(55, 1)),
         sg.Slider(range=(0,1), default_value=0.01, size=(20,15), orientation='horizontal', key="max_rear")], # INTEGER

        [sg.Text('Relative to Bounding Box', size=(55, 1)),
         sg.Checkbox('Relative to Bounding Box', default=True, size=(15, 1), key="max_dist_relative_scale")],

        [sg.Text('Average Normals', size=(55, 1)),
         sg.Checkbox('Average Normals', default=True, size=(15, 1), key="average_normals")],

        [sg.Text('Ignore Backface', size=(55, 1)),
         sg.Checkbox('Ignore Backface', default=True, size=(15, 1), key="ignore_backface")],


        [sg.Text('High Poly name suffix', size=(55, 1)),
         sg.Input(default_text = "_high", size=(20,15), key="name_suffix_high")], # STRING

        [sg.Text('Low Poly name suffix.', size=(55, 1)),
         sg.Input(default_text = "_low", size=(20,15), key="name_suffix_low")], # STRING

        [sg.Text('Output format', size=(55, 1)),
         sg.Combo(['surface', 'dds', 'bmp', 'jpg', 'jif', 'jpeg', 'jpe', 'png', 'tga', 'targa', 'tif', 'tiff', 'wap', 'wbmp', 'wbm', 'psd', 'psb', 'hdr', 'exr', 'webp'], default_value='jpg', size=(15, 1), key="output_format")],

         # ambient-occlusion options
        [sg.Text('                  ', size=(55, 2))],
        [sg.Text('# Ambient occlusion options.', size=(55, 2))],

        [sg.Text('Antialiasing method.', size=(55, 1)),
         sg.Combo(['None', 'Subsampling 2x2', 'Subsampling 4x4', 'Subsampling 8x8'], default_value='None', size=(15, 1), key="antialiasing")],





        [sg.Text('Enable Floor', size=(55, 1)),
         sg.Checkbox('Enable Floor', default=True, size=(15, 1), key="enable_ground_plane")],

        [sg.Text('Floor Offset.', size=(55, 1)),
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

    window = sg.Window('Sbsbaker Utility - 0.01 Alpha', layout)


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

                            for node in res:
                                # Generate parameters
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

                                args += ' --name-suffix-high ' + str(values['name_suffix_high']) # High Poly name suffix.
                                args += ' --name-suffix-low ' + str(values['name_suffix_low']) # Low Poly name suffix.
                                args += ' --output-format ' + str(values['output_format']) # Format to use for output image file.

                                output_path = values['output_path'];
                                if (output_path == '/'):
                                    output_path = os.path.join(file_path, '..')
                                args += ' --output-path "' + str(output_path) + '"'# Set the output path for the generated files. By default the output path is the current directory.

                                antialiasings = {
                                    'None': 0,
                                    'Subsampling 2x2': 1,
                                    'Subsampling 4x4': 2,
                                    'Subsampling 8x8': 3,
                                }
                                antialiasing = antialiasings.get(values['antialiasing'], 0)
                                args += ' --antialiasing ' + str(antialiasing) # Antialiasing method.

                                args += ' --enable-ground-plane ' + str(values['enable_ground_plane']).lower() # If enabled, adds an infinite plane under the baked mesh.
                                args += ' --ground-offset ' + str(values['ground_offset']) # Offset of the ground plane from the mesh lowest point.


                                # --self-occlusion
                                args += ' --output-name mat_' + node + '_ambient_occlusion' # Nodename
                                args += ' --input-selection ' + node # Nodename
                                args += ' --use-lowdef-as-highdef true' # Skip scene request

                                print('Exported ' + node)

                                # print(args)
                                subprocess.Popen(args)
            else:
                sg.popup_error('Please select a valid folder')

    window.Close()   # Don't forget to close your window!

if __name__ == '__main__':
    main()
