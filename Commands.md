Global options
--doc-html, --doc
Generate basic documentation html from the option's help.
--help, -h, -?
Display help about given subcommand. If no subcommand is provided, this help about global options is printed.
--opt-descr
Create json description of all available options
--quiet, -q
Disable warning messages.
--verbose, -v
Enable info and debug messages.
--version, -V
Display version of the program.
Subcommand ambient-occlusion
Input and output options
--disable-gpu <bool> [default: "no"]
Disable GPU Raytracing.
--force-dxr <bool> [default: "no"]
Force DXR Raytracing on video cards that support it partially.
--force-optix <bool> [default: "no"]
Force Optix Raytracing.
--input-selection <arg>
Select a submesh⁄subgroup of a mesh. Mesh subpart selection can be specified using this syntax for <arg>: <nodeName>@<materialId> where the additional @<materialId> is optional. If no material id is specified, all the ids will be used for the process. <nodeName> can either be the name of a mesh part or of a transform group. In this case, all the mesh parts parented directly or inderectly to this node will be used for the process.
--inputs <path>
Mesh files to process. This option is implicit, so you can just provide a list of files at the end of your arguments, they will be interpreted as inputs.
--name-suffix-high <name> [default: "_high"]
High Poly name suffix.
--name-suffix-low <name> [default: "_low"]
Low Poly name suffix.
--nodxr <bool> [default: "no"]
[Deprecated] Disable DirectX Raytracing.
--nooptix <bool> [default: "no"]
[Deprecated] Disable Optix raytracing.
--output-format <format> [default: "png"]
Format to use for output image file. Default='png'. Formats Supported: surface, dds, bmp, jpg, jif, jpeg, jpe, png, tga, targa, tif, tiff, wap, wbmp, wbm, psd, psb, hdr, exr, webp.
--output-name <name> [default: "{inputName}_{bakerName}"]
Set the output name of the generated files, without the extension."The name is "{inputName}_{bakerName}" by default. You can use the following patterns that will be replaced by the program when saving the result of the process: - {inputName}. Replaced by the input name. - {bakerName}. Replaced by the baker name. - {udim}. Replaced by the UDIM id of the baked tile (MARI convention).
--output-path <name> [default: ".⁄"]
Set the output path for the generated files. By default the output path is the current directory.You can use the following patterns that will be replaced by the program when saving the result of the process: - {inputPath}. Replaced by the path of the first processed sbs.
--per-fragment-binormal <bool> [default: "no"]
Controls whether the binormal of the tangent frame has to be computed in the fragment shader (true) or in the vertex shader (false). - Set by default to 'false' for unitytspace tangent space plugin. - Set by default to 'false' for mikktspace tangent space plugin. - Set by default to 'true' otherwise.
--recompute-tangents <bool> [default: "no"]
Force to recompute tangents; do not load tangents from the mesh if available.
--tangent-space-plugin <path> [default: "⁄home⁄colin⁄workspace⁄sat⁄dev⁄build⁄build-batchtools-Desktop-Debug⁄bin⁄libmikktspace.so"]
Set the plugin file used to compute the meshes tangent space frames.
ambient-occlusion options
--apply-diffusion <bool> [default: "true"]
Whether to use diffusion as a post-process after dilation, or not.
--details <float> [default: "0.6000000238418579"]
A lower value will be more precise but will easily produce artifacts.
--dilation-width <int> [default: "1"]
Width of the dilation post-process (in pixels) applied before diffusion.
--normal <string>
External normal map from file.
--normal-format, --normal-invert <int> [default: "1"]
Invert green component in normal map depending on selected format. (0='OpenGL', 1='DirectX') Please note that --normal-invert is now deprecated and will be removed in a future version.
--normal-invert <bool> [default: "false"]
Invert the normals.
--normal-world-space <bool> [default: "false"]
Tell if the normal map is in world space.
--output-size <w>,<h>
Output size of the generated map.<w> and <h> are the exponents of powers of 2 that give the actual width and height. In other words, you must provide the logarithm in base 2 of the actual width and height. For example '--output-size 10,11' means a 1024x2048 map.
--quality <int> [default: "1"]
Quality of the ambient occlusion. A higher quality is slower. (0='Low', 1='Medium', 2='High', 3='Very High')
--spread <float> [default: "0.009999999776482582"]
Spread of the ambient occlusion
--udim <udim>
Coordinates of the uv tile to compute, given as a UDIM id (MARI convention) (e.g "1022"). [default: "1001"]
--use-neighbors <bool> [default: "false"]
Use unselected mesh parts to compute the ambient occlusion.
--uv-set <int> [default: "0"]
Select UV set used to bake meshes information.
--uv-tile <u>,<v>
Coordinates of the uv tile to compute, given as two zero-based indices, e.g. "1,2". [default: "0,0"]
Subcommand ambient-occlusion-from-mesh
Input and output options
--disable-gpu <bool> [default: "no"]
Disable GPU Raytracing.
--force-dxr <bool> [default: "no"]
Force DXR Raytracing on video cards that support it partially.
--force-optix <bool> [default: "no"]
Force Optix Raytracing.
--input-selection <arg>
Select a submesh⁄subgroup of a mesh. Mesh subpart selection can be specified using this syntax for <arg>: <nodeName>@<materialId> where the additional @<materialId> is optional. If no material id is specified, all the ids will be used for the process. <nodeName> can either be the name of a mesh part or of a transform group. In this case, all the mesh parts parented directly or inderectly to this node will be used for the process.
--inputs <path>
Mesh files to process. This option is implicit, so you can just provide a list of files at the end of your arguments, they will be interpreted as inputs.
--name-suffix-high <name> [default: "_high"]
High Poly name suffix.
--name-suffix-low <name> [default: "_low"]
Low Poly name suffix.
--nodxr <bool> [default: "no"]
[Deprecated] Disable DirectX Raytracing.
--nooptix <bool> [default: "no"]
[Deprecated] Disable Optix raytracing.
--output-format <format> [default: "png"]
Format to use for output image file. Default='png'. Formats Supported: surface, dds, bmp, jpg, jif, jpeg, jpe, png, tga, targa, tif, tiff, wap, wbmp, wbm, psd, psb, hdr, exr, webp.
--output-name <name> [default: "{inputName}_{bakerName}"]
Set the output name of the generated files, without the extension."The name is "{inputName}_{bakerName}" by default. You can use the following patterns that will be replaced by the program when saving the result of the process: - {inputName}. Replaced by the input name. - {bakerName}. Replaced by the baker name. - {udim}. Replaced by the UDIM id of the baked tile (MARI convention).
--output-path <name> [default: ".⁄"]
Set the output path for the generated files. By default the output path is the current directory.You can use the following patterns that will be replaced by the program when saving the result of the process: - {inputPath}. Replaced by the path of the first processed sbs.
--per-fragment-binormal <bool> [default: "no"]
Controls whether the binormal of the tangent frame has to be computed in the fragment shader (true) or in the vertex shader (false). - Set by default to 'false' for unitytspace tangent space plugin. - Set by default to 'false' for mikktspace tangent space plugin. - Set by default to 'true' otherwise.
--recompute-tangents <bool> [default: "no"]
Force to recompute tangents; do not load tangents from the mesh if available.
--tangent-space-plugin <path> [default: "⁄home⁄colin⁄workspace⁄sat⁄dev⁄build⁄build-batchtools-Desktop-Debug⁄bin⁄libmikktspace.so"]
Set the plugin file used to compute the meshes tangent space frames.
ambient-occlusion-from-mesh options
--antialiasing <int> [default: "0"]
Antialiasing method. (0='None', 1='Subsampling 2x2', 2='Subsampling 4x4', 3='Subsampling 8x8')
--apply-diffusion <bool> [default: "true"]
Whether to use diffusion as a post-process after dilation, or not.
--attenuation <int> [default: "2"]
How occlusion is attenuated by occluder distance (0='None', 1='Smooth', 2='Linear')
--average-normals <bool> [default: "true"]
Compute rays directions based on averaged normals.
--cage-mesh <path>
Cage file..
--dilation-width <int> [default: "1"]
Width of the dilation post-process (in pixels) applied before diffusion.
--enable-ground-plane <bool> [default: "false"]
If enabled, adds an infinite plane under the baked mesh.
--ground-offset <float> [default: "0"]
Offset of the ground plane from the mesh lowest point.
--highdef-mesh <path>
High definition meshes..
--ignore-backface <bool> [default: "true"]
Ignore backfacing triangles when trying to match low and high resolution geometry.
--ignore-backface-secondary <int> [default: "0"]
Ignore backfacing triangles for occlusion rays. (0='Never', 1='Always', 2='By Mesh Name')
--invert-skew-correction <bool> [default: "false"]
If enabled, bright areas correspond to averaged direction and dark areas correspond to straight directions.
--match <int> [default: "0"]
Choose which method is used to match low and high resolution geometry. (0='Always', 1='By Mesh Name')
--max-dist <float> [default: "1"]
Maximum Occluder Distance.
--max-dist-relative-scale <bool> [default: "true"]
Interpret the Occluder Distance as a factor of the mesh bounding box.
--max-frontal <float> [default: "0.009999999776482582"]
Max frontal distance for raytracing.
--max-rear <float> [default: "0.009999999776482582"]
Max rear distance for raytracing.
--min-dist <float> [default: "9.999999747378752e-06"]
Minimum Occluder Distance (bias).
--nb-second-rays <int> [default: "64"]
Number of secondary rays (in [1; 256]).
--normal <string>
External normal map from file.
--normal-format, --normal-invert <int> [default: "1"]
Invert green component in normal map depending on selected format. (0='OpenGL', 1='DirectX') Please note that --normal-invert is now deprecated and will be removed in a future version.
--normal-world-space <bool> [default: "false"]
Tell if the normal map is in world space.
--output-size <w>,<h>
Output size of the generated map.<w> and <h> are the exponents of powers of 2 that give the actual width and height. In other words, you must provide the logarithm in base 2 of the actual width and height. For example '--output-size 10,11' means a 1024x2048 map.
--ray-distrib <int> [default: "1"]
Angular Distribution of Occlusion Rays. (0='Uniform', 1='Cosine')
--relative-to-bbox <bool> [default: "true"]
Interpret the max distances as a factor of the mesh bounding box.
--self-occlusion <int> [default: "0"]
Choose what geometry will cause occlusion. (0='Always', 1='Only Same Mesh Name')
--skew-correction <bool> [default: "false"]
Straighten rays direction based on a grayscale texture to avoid projection deformation.
--skew-map <string>
External skew texture from file.
--spread-angle <float> [default: "180"]
Maximum spread angle of occlusion rays.
--udim <udim>
Coordinates of the uv tile to compute, given as a UDIM id (MARI convention) (e.g "1022"). [default: "1001"]
--use-cage <bool> [default: "false"]
Use cage to cast rays.
--use-lowdef-as-highdef <bool> [default: "false"]
Use the low poly mesh as the high poly mesh.
--uv-set <int> [default: "0"]
Select UV set used to bake meshes information.
--uv-tile <u>,<v>
Coordinates of the uv tile to compute, given as two zero-based indices, e.g. "1,2". [default: "0,0"]
Subcommand bent-normal-from-mesh
