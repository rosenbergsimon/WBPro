import os
import requests
import datetime as dt


# runs the entire api call and returns an orderly dictionary with relevant information.
def return_students(ident):
    key = os.environ.get("WBPRO_CODE")
    # search for open flights starts one hour before current time. 3 hours before now. FL uses Zulu time
    start_search = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)
    start_search = start_search.replace(tzinfo=None)

    start_search = start_search.isoformat(timespec='seconds') + "Z"

    end_search = dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=12)
    end_search = end_search.replace(tzinfo=None)
    end_search = end_search.isoformat(timespec='seconds') + "Z"

    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    query = f"""
        {{
          bookings(from: "{start_search}", to: "{end_search}", first: 60, subtypes: [SINGLE_STUDENT, MULTI_STUDENT, RENTAL, OPERATION], all: true, statuses: [OPEN]) 
          {{
            nodes {{
              __typename
              ... on AircraftBooking {{
                aircraft {{
                  callSign	
                }}
                flightStartsAt
              }}
              ... on SingleStudentBooking {{  
                instructor {{
                  firstName
                  lastName 
                }}
                student {{
                  firstName
                  lastName
                  id
                }}
                plannedLesson {{
                  userProgram {{
                    id
                  }}
                  id
                }}
              }}
              ... on MultiStudentBooking {{
                instructor {{
                  firstName
                  lastName
                }}
                students {{
                  firstName
                  lastName
                  id
                }}
                plannedLessons {{
                  student {{
                    id
                  }}
                  userProgram {{
                    id
                  }}
                  id
                }}
              }}
              ... on OperationBooking {{
                pic {{
                  firstName
                  lastName
                }}
                id
              }}
              ... on RentalBooking {{
                renter {{
                  firstName
                  lastName
                }}
                id
              }}
            }}
          }}
        }}

        """

    response = requests.post(url="https://api.flightlogger.net/graphql", headers=headers, json={"query": query})

    json_response = response.json()

    same_aircraft_items = []  # for flights on same plane, will put them here.

    for i in json_response['data']['bookings']['nodes']:
        if i['__typename'] == "OperationBooking" or i['__typename'] == "RentalBooking":
            if i['aircraft']['callSign'] == ident:
                same_aircraft_items.append(i)
        # can't have a None type for logic elsewhere. '0' works better. This happens if booking has no lesson
        # attached to it by the instructor.
        if i['__typename'] == "SingleStudentBooking":
            if i['plannedLesson'] is None:
                i['plannedLesson'] = {'userProgram': {'id': '0'}, 'id': '0'}
            if i['aircraft']['callSign'] == ident:
                same_aircraft_items.append(i)
        if i['__typename'] == 'MultiStudentBooking':
            if len(i['plannedLessons']) <= 1:
                i['plannedLessons'] = [{'student': {'id': '0'}, 'userProgram': {'id': '0'}, 'id': '0'},
                                       {'student': {'id': '0'}, 'userProgram': {'id': '0'}, 'id': '0'}]
            if i['aircraft']['callSign'] == ident:
                same_aircraft_items.append(i)

    params_list = []

    for i in same_aircraft_items:
        if i['__typename'] == 'OperationBooking':
            params_list.append({'flight_type': i['__typename'], 'time': i['flightStartsAt'],
                                'student': i['pic']['firstName'] + " " + i['pic']['lastName'], 'id': i['id']})

        if i['__typename'] == 'RentalBooking':
            params_list.append({'flight_type': i['__typename'], 'time': i['flightStartsAt'],
                                'student': i['renter']['firstName'] + " " + i['renter']['lastName'], 'id': i['id']})

        if i['__typename'] == 'SingleStudentBooking':
            params_list.append({'student': i['student']['firstName'] + " " + i['student']['lastName'],
                                'instructor': i['instructor']['firstName'] + " " + i['instructor']['lastName'],
                                'codes': [i['student']['id'], i['plannedLesson']['userProgram']['id'],
                                          i['plannedLesson']['id']], 'flight_type': i['__typename'],
                                'time': i['flightStartsAt']})

        if i['__typename'] == 'MultiStudentBooking':
            if i['students'][0]['id'] == i['plannedLessons'][1]['student']['id']:
                i['plannedLessons'] = [i['plannedLessons'][1], i['plannedLessons'][0]]
            params_list.append({'student': i['students'][0]['firstName'] + " " + i['students'][0]['lastName'],
                                'instructor': i['instructor']['firstName'] + " " + i['instructor']['lastName'],
                                'codes': [i['students'][0]['id'], i['plannedLessons'][0]['userProgram']['id'],
                                          i['plannedLessons'][0]['id']], 'flight_type': i['__typename'],
                                'time': i['flightStartsAt']})
            params_list.append({'student': i['students'][1]['firstName'] + " " + i['students'][1]['lastName'],
                                'instructor': i['instructor']['firstName'] + " " + i['instructor']['lastName'],
                                'codes': [i['students'][1]['id'], i['plannedLessons'][1]['userProgram']['id'],
                                          i['plannedLessons'][1]['id']], 'flight_type': i['__typename'],
                                'time': i['flightStartsAt']})

    return params_list
