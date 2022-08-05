"""
SEMRinterface/views.py
version 3.0
package github.com/ajk77/SimpleEMRSystem
Modified by AndrewJKing.com|@andrewsjourney

This is the view processing file.

---LICENSE---
This file is part of SimpleEMRSystem

SimpleEMRSystem is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

SimpleEMRSystem is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SimpleEMRSystem.  If not, see <https://www.gnu.org/licenses/>.
"""
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie
import os.path
import json

# Global variables
dir_local = os.getcwd()
dir_resources = os.path.join(dir_local, "resources")


def select_study(request):
    print(request.path_info)
    from SEMRinterface.utils import get_list_study_id

    list_study_id = get_list_study_id(dir_resources)

    template = loader.get_template(os.path.join(
        'SEMRinterface', 'study_selection_screen.html'))
    context_dict = {
        'list_study_id': list_study_id,
        'test': 'test'
    }
    return HttpResponse(template.render(context_dict))


def select_user(request, study_id):
    print(request.path_info)

    dir_study_user_details = os.path.join(
        dir_resources, study_id, 'user_details.json')
    with open(dir_study_user_details) as f:
        dict_user_2_details = json.load(f)

    template = loader.get_template(os.path.join(
        'SEMRinterface', 'user_selection_screen.html'))
    context_dict = {
        'dict_user_2_details': dict_user_2_details,
        'study_id': study_id,
        'test': 'test'
    }
    return HttpResponse(template.render(context_dict))


def select_case(request, study_id, user_id):
    print(request.path_info)

    dir_study_user_details = os.path.join(
        dir_resources, study_id, 'user_details.json')
    with open(dir_study_user_details) as f:
        dict_user_2_details = json.load(f)
    
    dir_study_admitting_diagnoses = os.path.join(
        dir_resources, study_id, 'admitting_diagnoses.json')
    with open(dir_study_admitting_diagnoses) as fp:
        admitting_diagnoses_dict = json.load(fp)

    patient_ages = {}
    studies = os.path.join(
        dir_resources, study_id, 'cases_all')
    patient_dirs = os.scandir(studies)
    for patient_dir in patient_dirs:
        patient_demographics = os.path.join(patient_dir.path, "demographics.json")
        with open(patient_demographics) as fp:
            demographics = json.load(fp)
            patient_ages[int(patient_dir.name)] = demographics["age"]

    list_cases_assigned = dict_user_2_details[user_id]['cases_assigned']
    list_cases_completed = dict_user_2_details[user_id]['cases_completed']

    template = loader.get_template('SEMRinterface/case_selection_screen.html')
    context_dict = {
        'list_cases_assigned': list_cases_assigned,
        'list_cases_completed': list_cases_completed,
        'admitting_diagnoses': admitting_diagnoses_dict,
        'patient_ages': patient_ages,
        'user_id': user_id,
        'study_id': study_id,
        'test': 'test'
    }
    return HttpResponse(template.render(context_dict))


def case_reset(request):
    print(request.path_info)

    # if request.is_ajax():
    message = " in case_reset "
    if request.method == 'GET':

        # load GET vars #
        study_id = request.GET['study_id']
        user_id = request.GET['user_id']
        case_id = request.GET['case_id']

        # load user details #
        dir_study_user_details = os.path.join(
            dir_resources, study_id, 'user_details.json')
        with open(dir_study_user_details) as f:
            dict_user_2_details = json.load(f)

        # remove case from completed list #
        dict_user_2_details[user_id]['cases_completed'].remove(case_id)

        # save user details #
        with open(dir_study_user_details, 'w') as f:
            json.dump(dict_user_2_details, f)

        message = "case_reset = SUCCESS"

    else:
        message = "not a GET. No action performed."

    return HttpResponse(message)


def mark_complete(request):
    print(request.path_info)

    # if request.is_ajax():
    message = " in mark_complete "
    if request.method == 'GET':

        # load GET vars #
        study_id = request.GET['study_id']
        user_id = request.GET['user_id']
        case_id = request.GET['case_id']

        # load user details #
        dir_study_user_details = os.path.join(
            dir_resources, study_id, 'user_details.json')
        with open(dir_study_user_details) as f:
            dict_user_2_details = json.load(f)

        # remove case from completed list #
        dict_user_2_details[user_id]['cases_completed'].append(case_id)

        # save user details #
        with open(dir_study_user_details, 'w') as f:
            json.dump(dict_user_2_details, f)

        message = "mark_complete = SUCCESS"

    else:
        message = "not a GET. No action performed."

    return HttpResponse(message)


def mark_complete_url(request, study_id, user_id, case_id):
    print(request.path_info)

    dir_study_user_details = os.path.join(
        dir_resources, study_id, 'user_details.json')
    with open(dir_study_user_details) as f:
        dict_user_2_details = json.load(f)

    # remove case from completed list #
    dict_user_2_details[user_id]['cases_completed'].append(case_id)

    # save user details #
    with open(dir_study_user_details, 'w') as f:
        json.dump(dict_user_2_details, f)

    return select_case(request, study_id, user_id)


'''
@api_view(['POST'])
def save_selected_items(request, study_id, user_id, case_id):
    if request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        print(tutorial_data)
        return JsonResponse('good', status=status.HTTP_201_CREATED)
        return JsonResponse('bad', status=status.HTTP_400_BAD_REQUEST)


'''


def save_selected_items(request, study_id, user_id, case_id):
    if request.is_ajax():
        message = "Yes, AJAX!"
        if request.method == 'POST':
            selected_ids = json.loads(request.POST.get("selected_ids"))
            dir_study_stored_results = os.path.join(
                dir_resources, study_id, 'stored_results.txt')
            with open(dir_study_stored_results, 'a+') as f:
                f.write(json.dumps(
                    {"user_id": user_id, "case_id": case_id, "selected_ids": selected_ids}) + '\n')
    else:
        message = "Not Ajax"

    return HttpResponse(message)


@ensure_csrf_cookie
def case_viewer(request, study_id, user_id, case_id, time_step=0):
    print(request.path_info)
    time_step = int(time_step)

    ## load global files ##
    load_dir = os.path.join(dir_resources, study_id)
    dict_case_2_details = json.load(
        open(os.path.join(load_dir, 'case_details.json'), 'r'))
    dict_data_layout = json.load(
        open(os.path.join(load_dir, 'data_layout.json'), 'r'))
    dict_user_2_details = json.load(
        open(os.path.join(load_dir, 'user_details.json'), 'r'))
    dict_variable_2_details = json.load(
        open(os.path.join(load_dir, 'variable_details.json'), 'r'))

    ## load case specific files ##
    load_dir = os.path.join(dir_resources, study_id, 'cases_all', case_id)
    dict_demographics = json.load(
        open(os.path.join(load_dir, 'demographics.json'), 'r'))
    dict_notes = json.load(
        open(os.path.join(load_dir, 'note_panel_data.json'), 'r'))
    dict_observations = json.load(
        open(os.path.join(load_dir, 'observations.json'), 'r'))

    ## define user instructions dict ##
    instructions = {}
    instructions["familiar"] = "Please use the available information to become familiar with this patient."
    instructions["select"] = "Please select the information you used when preparing to present this case."

    # Translating None to "null" within dict_variable_2_details, as the js call to add_observation_chart
    # cannot figure out how to deal with None.
    for key in dict_variable_2_details:
        min_y = dict_variable_2_details[key]["dflt_y_axis_ranges"][0]
        max_y = dict_variable_2_details[key]["dflt_y_axis_ranges"][1]
        if min_y == None:
            dict_variable_2_details[key]["dflt_y_axis_ranges"][0] = "null"
        if max_y == None:
            dict_variable_2_details[key]["dflt_y_axis_ranges"][1] = "null"

    # This provides a way to associate the notes  with the tab they're in 
    foo = list(dict_notes.keys())

    enumerated_note_headers = {}
    i = 0
    while i < len(foo):
        enumerated_note_headers[i] = foo[i - 1]
        i += 1

    template = loader.get_template('SEMRinterface/case_viewer.html')
    context_dict = {
        'case_id': case_id,
        'user_id': user_id,
        'study_id': study_id,
        'time_step': time_step,
        'show_checkboxes': dict_case_2_details[case_id][time_step]["check_boxes"],
        'instructions': instructions[dict_case_2_details[case_id][time_step]["instruction_set"]],
        'dict_case_details': dict_case_2_details[case_id],
        'dict_data_layout': dict_data_layout,
        'dict_user_details': dict_user_2_details[user_id],
        'dict_variable_2_details': dict_variable_2_details,
        'dict_demographics': dict_demographics,
        'dict_enumerated_note_headers': foo,
        'dict_notes': dict_notes,
        'dict_observations': dict_observations,
        'test': 'test',
        'list_1_2': [1, 2],
        'list_3_4_5_6': [3, 4, 5, 6]
    }
    return HttpResponse(template.render(context_dict))