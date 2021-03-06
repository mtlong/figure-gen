import os
from . import html_element, html_plot, chartjs
'''
in HTML format we
 - ignore background colors for whole figure (for now), the background color is white
 - do not support 'dashed' frames - if a frame is 'dashed' the frame will be normal (but still has a frame)
 - only support text rotation by 0° and +-90°
 - have plot defaults, that ignore some user defined input:
    * grid: lightgrey, fine lines
    * no upper and right axis
'''
def html_header_and_styles():
    header_lines = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',

        '<script src="./scripts/Chart.min.js"></script>' # TODO actually copy the file

        '<style type="text/css">',
        '.module { position: absolute; }',
        '.title-container { position: absolute; margin-top: 0; margin-bottom: 0;'
                           'display: flex; align-items: center; justify-content: center}',
        '.title-content { margin-top: 0; margin-bottom: 0; }',
        '.element { position: absolute; }',
        '</style>',

        '</head>',
        ''
    ]
    return "\n".join(header_lines)


def gen_grid_content(module_data, to_path):
    body = ''
    body += html_element.gen_images(module_data, to_path)
    body += html_element.gen_south_captions(module_data)
    body += html_element.gen_titles(module_data)
    body += html_element.gen_row_titles(module_data)
    body += html_element.gen_column_titles(module_data)
    return body

def gen_plot_content(module_data, id):
    body = ''
    body += html_plot.create_canvas(module_data, id)
    body += html_plot.create_script(module_data, id)
    return body

def gen_body_content(module_data, to_path, offset_top, offset_left, id):
    body = html_element.gen_module_unit_mm(module_data['total_width'], module_data['total_height'], offset_top, offset_left)

    if module_data['type'] == 'grid':
        body += gen_grid_content(module_data, to_path)
    else:
        body += gen_plot_content(module_data, id)

    return body + '\n' + '</div>'

def generate(module_data, to_path, figure_idx, module_idx, temp_folder, delete_gen_files=False, tex_packages=[]):
    return module_data

def combine(data, filename, temp_folder, delete_gen_files=False):
    to_path = os.path.dirname(filename)

    html_code = html_header_and_styles()
    html_code += '<body>' + '\n'

    # Create a container div so the result can be embedded
    sum_total_width_mm = 0
    for d in data[0]:
        sum_total_width_mm += d['total_width']
    figure_height = 0.
    for d in data:
        figure_height += d[0]['total_height']
    html_code += f"<div style='position: relative; background-color: white; width: {sum_total_width_mm}mm; height: {figure_height}mm; ' > \n"

    offset_top = 0
    for fig_idx in range(len(data)):
        offset_left = 0
        module_index = 0
        for module in data[fig_idx]:
            html_code += gen_body_content(module, to_path, offset_top=offset_top, offset_left=offset_left, id=module_index) + '\n'
            offset_left += module['total_width']
            module_index += 1
        offset_top += data[fig_idx][0]['total_height']

    html_code += '\n' + '</div></body></html>'

    with open(filename, "w") as file:
        file.write(html_code)

    chartjs.emit(to_path)