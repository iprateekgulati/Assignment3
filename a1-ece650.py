import sys
import re
import ast

from decimal import Decimal

database = dict()


def can_change(x):
    if x in database:
        return True
    else:
        return False

def can_add(x):
    if x in database:
        return False
    else:
        return True


def case_insesitive(x):
    y = x.lower()
    return y


def add_street(x, y):
    if (can_add(x)):
        if (Is_valid_street(x)):
            if (do_parentheses_match(y)):
                y = re.sub(' +', '', y)
                y = re.sub('\)\(', ') ( ', y)
                y = re.sub('\( ', '(', y)
                y = y.split(' ')
                if all(Is_valid_location(i) for i in y):
                    database[x] = y
                else:
                    print "Error: enter valid vertices"
            else:
                print "Error: Check for paranthesis"
        else:
            print "Error: Please enter correct command"
    else:
        print "Error: Street Currently exist"


def change_street(x, y):
    z = can_change(x)
    if (z == True):
        if (Is_valid_street(x)):
            if (do_parentheses_match(y)):
                y = re.sub(' +', '', y)
                y = re.sub('\)\(', ') ( ', y)
                y = re.sub('\( ', '(', y)
                y = y.split(' ')
                if all(Is_valid_location(i) for i in y):
                    database[x] = y
                else:
                    print "Error: enter valid vertices"
            else:
                print "Error: Check for paranthesis"
        else:
            print "Error: Enter again"
    else:
        print "Error: 'c' or 'r' specified for a street that does not exist."


def remove_street(x):
    try:
        del database[x]
    except KeyError:
        sys.stderr.write("Error: " + x + " Street not Found to delete" + "\n")


def Is_valid_street(street):
    if all(x.isalpha() or x.isspace() for x in street):
        return True
    else:
        return False


def do_parentheses_match(input_string):
    s = []
    balanced = True
    index = 0
    while index < len(input_string) and balanced:
        token = input_string[index]
        if token == "(":
            s.append(token)
        elif token == ")":
            if len(s) == 0:
                balanced = False
            else:
                s.pop()

        index += 1

    return balanced and len(s) == 0


def Is_valid_location(x):
    regex = r'\(-?\d+,-?\d+\)'
    preg = re.compile(regex)
    if (preg.match(x)):
        return True
    else:
        return False


def display_graph():
    vertices = list()
    list_vertices = list()
    graph_edges = list()
    graph_edgeset = set()
    graph_set = set()
    duplicate_edges = list()
    vertex_list = dict()
    duplicate_edges1=list()
    list_intersection = list()
    vertices_intersection = list()
    y = list()

    coordinates_st1 = 1
    coordinates_st2 = 1
    mylist = list(database.values())
    no_street_names = len(mylist)
    vertices = [None] * no_street_names
    for o in range(0, no_street_names):
        y = [i.split(', ', 1)[0] for i in mylist[o]]

        vertices[o] = y
    for i in range(0, no_street_names):

        for j in range(i + 1, no_street_names):
            w = len(vertices[i])

            v = len(vertices[j])
            while coordinates_st1 < w:
                while coordinates_st2 < v:
                    coordinate1 = vertices[i][coordinates_st1 - 1]
                    coordinate2 = vertices[i][coordinates_st1]
                    coordinate3 = vertices[j][coordinates_st2 - 1]
                    coordinate4 = vertices[j][coordinates_st2]
                    x1, y1 = ast.literal_eval(coordinate1)
                    x2, y2 = ast.literal_eval(coordinate2)
                    x3, y3 = ast.literal_eval(coordinate3)
                    x4, y4 = ast.literal_eval(coordinate4)
                    x1, x2, x3, x4, y1, y2, y3, y4 = float(x1), float(x2), float(x3), float(x4), float(y1), float(
                        y2), float(y3), float(y4)
                    y1_diff = y2 - y1
                    x1_diff = x1 - x2
                    xy1_diff = y1_diff * (x1) + x1_diff * (y1)

                    y2_diff = y4 - y3
                    x2_diff = x3 - x4
                    xy2_diff = y2_diff * (x3) + x2_diff * (y3)
                    determinant = y1_diff * x2_diff - y2_diff * x1_diff
                    min_x1 = min(x1, x2)
                    min_x2 = min(x3, x4)
                    max_x1 = max(x1, x2)
                    max_x2 = max(x3, x4)
                    min_y1 = min(y1, y2)
                    min_y2 = min(y3, y4)
                    max_y1 = max(y1, y2)
                    max_y2 = max(y3, y4)
                    cond1 = False
                    cond2 = False

                    coordinate1 = "(" + str(x1) + "," + str(y1) + ")"
                    coordinate2 = "(" + str(x2) + "," + str(y2) + ")"
                    coordinate3 = "(" + str(x3) + "," + str(y3) + ")"
                    coordinate4 = "(" + str(x4) + "," + str(y4) + ")"
                    list_coordinates = list((coordinate1, coordinate2, coordinate3, coordinate4))

                    if (determinant != 0):
                        X = Decimal((x2_diff * xy1_diff - x1_diff * xy2_diff) / determinant)
                        X = round(X, 2)
                        Y = Decimal((y1_diff * xy2_diff - y2_diff * xy1_diff) / determinant)
                        Y = round(Y, 2)

                        if (bool(X <= max_x1) & bool(X >= min_x1)):

                            if (bool(Y <= max_y1) & bool(Y >= min_y1)):
                                cond1 = True
                            if (bool(X <= max_x2) & bool(X >= min_x2)):

                                if (bool(Y <= max_y2) & bool(Y >= min_y2)):
                                    cond2 = True
                        if (cond1 == True & cond2 == True):

                            intersection = "(" + str(X) + "," + str(Y) + ")"
                            list_vertices.extend(list_coordinates)
                            list_intersection.append(intersection)
                            vertices_intersection.append(list_coordinates)
                            list_vertices.append(intersection)
                            graph_set = set(list_vertices)
                            list_vertices = list(graph_set)
                            for z in range(0, len(list_vertices)):
                                vertex_list[z] = list_vertices[z]



                        else:
                            pass
                    elif (coordinate1 == coordinate4):

                        intersection = "(" + str(x4) + "," + str(y4) + ")"
                        list_vertices.extend(list_coordinates)
                        list_intersection.append(intersection)
                        vertices_intersection.append(list_coordinates)
                        list_vertices.append(intersection)
                        graph_set = set(list_vertices)
                        list_vertices = list(graph_set)
                        for z in range(0, len(list_vertices)):
                            vertex_list[z + 1] = list_vertices[z]
                    elif (coordinate2 == coordinate3):
                        intersection = "(" + str(x3) + "," + str(y3) + ")"
                        list_vertices.extend(list_coordinates)
                        list_intersection.append(intersection)
                        vertices_intersection.append(list_coordinates)
                        list_vertices.append(intersection)
                        graph_set = set(list_vertices)
                        list_vertices = list(graph_set)
                        for z in range(0, len(list_vertices)):
                            vertex_list[z] = list_vertices[z]

                    elif (x1 == x2 == x3 == x4):
                        y_range1 = abs(y2 - y1)
                        y_range2 = abs(y4 - y3)
                        if (y_range1 > y_range2):
                            big_line = 1
                        elif (y_range2 > y_range1):
                            big_line = 2
                        if (big_line == 1):
                            if (y3 > min_y1 and y3 < max_y1):
                                intersection = "(" + str(x3) + "," + str(y3) + ")"
                                list_vertices.extend(list_coordinates)
                                list_intersection.append(intersection)
                                vertices_intersection.append(list_coordinates)
                                list_vertices.append(intersection)
                                graph_set = set(list_vertices)
                                list_vertices = list(graph_set)
                                for z in range(0, len(list_vertices)):
                                    vertex_list[z + 1] = list_vertices[z]
                            if (y4 > min_y1 and y4 < max_y1):
                                intersection = "(" + str(x4) + "," + str(y4) + ")"
                                list_vertices.extend(list_coordinates)
                                list_intersection.append(intersection)
                                vertices_intersection.append(list_coordinates)
                                list_vertices.append(intersection)
                                graph_set = set(list_vertices)
                                list_vertices = list(graph_set)
                                for z in range(0, len(list_vertices)):
                                    vertex_list[z] = list_vertices[z]

                        if (big_line == 2):
                            if (y1 > min_y2 and y1 < max_y2):
                                intersection = "(" + str(x1) + "," + str(y1) + ")"
                                list_vertices.extend(list_coordinates)
                                list_intersection.append(intersection)
                                vertices_intersection.append(list_coordinates)
                                list_vertices.append(intersection)
                                graph_set = set(list_vertices)
                                list_vertices = list(graph_set)
                                for z in range(0, len(list_vertices)):
                                    vertex_list[z] = list_vertices[z]
                            if (y2 > min_y2 and y2 < max_y2):
                                intersection = "(" + str(x2) + "," + str(y2) + ")"
                                list_vertices.extend(list_coordinates)
                                list_intersection.append(intersection)
                                vertices_intersection.append(list_coordinates)
                                list_vertices.append(intersection)
                                graph_set = set(list_vertices)
                                list_vertices = list(graph_set)
                                for z in range(0, len(list_vertices)):
                                    vertex_list[z] = list_vertices[z]

                    elif (y1 == y2 == y3 == y4):
                        x_range1 = abs(x2 - x1)
                        x_range2 = abs(x4 - x3)
                        if (x_range1 > x_range2):
                            big_line = 1
                        elif (x_range2 > x_range1):
                            big_line = 2
                        if (big_line == 1):
                            if (x3 > min_x1 and x3 < max_x1):
                                intersection = "(" + str(x3) + "," + str(y3) + ")"
                                list_vertices.extend(list_coordinates)
                                list_intersection.append(intersection)
                                vertices_intersection.append(list_coordinates)
                                list_vertices.append(intersection)
                                graph_set = set(list_vertices)
                                list_vertices = list(graph_set)
                                for z in range(0, len(list_vertices)):
                                    vertex_list[z] = list_vertices[z]
                            if (x4 > min_x1 and x4 < max_x1):
                                intersection = "(" + str(x4) + "," + str(y4) + ")"
                                list_vertices.extend(list_coordinates)
                                list_intersection.append(intersection)
                                vertices_intersection.append(list_coordinates)
                                list_vertices.append(intersection)
                                graph_set = set(list_vertices)
                                list_vertices = list(graph_set)
                                for z in range(0, len(list_vertices)):
                                    vertex_list[z] = list_vertices[z]

                        if (big_line == 2):
                            if (x1 > min_x2 and x1 < max_x2):
                                intersection = "(" + str(x1) + "," + str(y1) + ")"
                                list_vertices.extend(list_coordinates)
                                list_intersection.append(intersection)
                                vertices_intersection.append(list_coordinates)
                                list_vertices.append(intersection)
                                graph_set = set(list_vertices)
                                list_vertices = list(graph_set)
                                for z in range(0, len(list_vertices)):
                                    vertex_list[z] = list_vertices[z]

                            if (x2 > min_x2 and x2 < max_x2):
                                intersection = "(" + str(x2) + "," + str(y2) + ")"
                                list_vertices.extend(list_coordinates)
                                list_intersection.append(intersection)
                                vertices_intersection.append(list_coordinates)
                                list_vertices.append(intersection)
                                graph_set = set(list_vertices)
                                list_vertices = list(graph_set)
                                for z in range(0, len(list_vertices)):
                                    vertex_list[z] = list_vertices[z]


                    coordinates_st2 = coordinates_st2 + 1
                coordinates_st1 = coordinates_st1 + 1
                coordinates_st2 = 1
            coordinates_st1 = 1

    sys.stdout.write("V ")
    sys.stdout.flush()
    sys.stderr.write("V ")
    sys.stdout.flush()
    sys.stdout.write(str(len(vertex_list)))
    sys.stdout.flush()
    sys.stderr.write(str(len(vertex_list)) + '\n')
    sys.stdout.flush()
    

    for t in range(0, len(list_intersection)):
        intersection_pt = list_intersection[t]
        vertexlist = vertices_intersection[t]
        [coordinate1, coordinate2, coordinate3, coordinate4] = vertexlist
        for g in vertex_list:

            if intersection_pt == vertex_list[g]:
                edge_intersection = g
        for s, e in vertex_list.items():
            if e == coordinate1:
                edge_coordinate1 = s

        for s, e in vertex_list.items():
            if e == coordinate2:
                edge_coordinate2 = s

        for s, e in vertex_list.items():
            if e == coordinate3:
                edge_coordinate3 = s

        for s, e in vertex_list.items():
            if e == coordinate4:
                edge_coordinate4 = s

        edge1 = "<" + str(edge_intersection) + "," + str(edge_coordinate1) + ">"

        edge2 = "<" + str(edge_intersection) + "," + str(edge_coordinate2) + ">"
        edge3 = "<" + str(edge_intersection) + "," + str(edge_coordinate3) + ">"
        edge4 = "<" + str(edge_intersection) + "," + str(edge_coordinate4) + ">"

        edgelist = list((edge1, edge2, edge3, edge4))
        graph_edges.extend(edgelist)
        graph_edgeset = set(graph_edges)
        graph_edges = list(graph_edgeset)
        distinct = list()



    for g in range(0,len(graph_edges)):
        edge_1 = graph_edges[g]
        edge_1 = re.sub('<', '(', edge_1)
        edge_1 = re.sub('>', ')', edge_1)
        pair1,pair2 = ast.literal_eval(edge_1)
        if(pair1==pair2):
            delete="<" + str(pair1) + "," + str(pair2) + ">"
            duplicate_edges.append(delete)

    for x in range(0, len(graph_edges)):
        edge = graph_edges[x]
        edge = re.sub('<', '(', edge)
        edge = re.sub('>', ')', edge)
        p1, p2 = ast.literal_eval(edge)

        for i in vertex_list:
            vertex1 = vertex_list[p1]

            vertex2 = vertex_list[p2]

            v_x1, v_y1 = ast.literal_eval(vertex1)
            v_x2, v_y2 = ast.literal_eval(vertex2)
            min_x1 = min(v_x1, v_x2)
            max_x1 = max(v_x1, v_x2)
            min_y1 = min(v_y1, v_y2)
            max_y1 = max(v_y1, v_y2)
            check_p = vertex_list[i]

            c_x, c_y = ast.literal_eval(check_p)
            if ((bool(c_x != min_x1) & bool(c_x != max_x1)) | ((bool(c_y != min_y1) & bool(c_y != max_y1)))):
                if (bool(c_x <= max_x1) & bool(c_x >= min_x1)):
                    if (bool(c_y <= max_y1) & bool(c_y >= min_y1)):
                        del_check = "<" + str(p1) + "," + str(p2) + ">"

                        duplicate_edges.append(del_check)
                        duplicate_edges_set = set(duplicate_edges)
                        duplicate_edges = list(duplicate_edges_set)

    for g in range(0, len(duplicate_edges)):
        graph_edges.remove(duplicate_edges[g])

    for l in range(0, len(graph_edges)):
        for l1 in range(l + 1, len(graph_edges)):
            edge_1 = graph_edges[l]
            edge_1 = re.sub('<', '(', edge_1)
            edge_1 = re.sub('>', ')', edge_1)
            pair1, pair2 = ast.literal_eval(edge_1)
            edge_2 = graph_edges[l1]
            edge_2 = re.sub('<', '(', edge_2)
            edge_2 = re.sub('>', ')', edge_2)
            pair3, pair4 = ast.literal_eval(edge_2)
            if (pair1 == pair4 and pair2 == pair3):
                delete = "<" + str(pair1) + "," + str(pair2) + ">"
                duplicate_edges1.append(delete)
                duplicate_edges_set1 = set(duplicate_edges1)
                duplicate_edges1 = list(duplicate_edges_set1)

    for m in range(0, len(duplicate_edges1)):
        graph_edges.remove(duplicate_edges1[m])
    for n in range(0, len(graph_edges)):
        coordinate = graph_edges[n]
        coordinate = re.sub('<', '(', coordinate)
        coordinate = re.sub('>', ')', coordinate)
        v1, w1 = ast.literal_eval(coordinate)
        distinct.append(v1)
        distinct_set = set(distinct)
        distinct = list(distinct_set)
        for n1 in range(0, len(distinct)):
            for n2 in range(n1 + 1, len(distinct)):
                edge_betweeen = "<" + str(distinct[n1]) + "," + str(distinct[n2]) + ">"
                graph_edges.append(edge_betweeen)
                graph_set = set(graph_edges)
                graph_edges = list(graph_set)

    sys.stdout.write("E {")
    sys.stdout.flush()
    sys.stderr.write("E {")
    sys.stdout.flush()
    count=len(graph_edges)
    for u in graph_edges:
        sys.stdout.write(u)
	sys.stderr.write(u)
        sys.stdout.flush()
        count=count-1
        if(count):
            sys.stdout.write(',')
	    sys.stderr.write(',')
            sys.stdout.flush()
    sys.stdout.write("}" + '\n')
    sys.stderr.write("}" + '\n')
    sys.stdout.flush()

def input():
    command=sys.stdin.readline()
    return command.replace('\n','')


def main():
    while True:
        user_input = input()
        if (user_input == ''):
            break
        elif (user_input[0] == 'r'):
            regexp = re.split(' +"|"|', user_input)
        else:
            regexp = re.split('" +| +"', user_input)
        if (len(regexp) == 1):
            command = regexp[0]
        elif (len(regexp) == 2):
            command = regexp[0]
            street_name = regexp[1]
            street_name = case_insesitive(street_name)
        elif (len(regexp) == 3):
            command = regexp[0]
            street_name = regexp[1]
            street_name = case_insesitive(street_name)
            gps_coordinates = regexp[2]
        else:
            sys.stdout.write("Error: " + "Wrong selection of user_input" + "\n")
            sys.stdout.flush()
            continue

        if command == 'a':
            try:
                add_street(street_name, gps_coordinates)
            except UnboundLocalError:
                sys.stderr.write("Error: " + "please enter full command!" + "\n")
                sys.stdout.flush()


        elif command == 'c':
            try:
                change_street(street_name, gps_coordinates)
            except UnboundLocalError:
                sys.stderr.write("Error: " + "please enter full command!" + "\n")
                sys.stdout.flush()

        elif command == 'r':
            try:
                remove_street(street_name)
            except UnboundLocalError:
                sys.stderr.write("Error: " + "please enter full command!" + "\n")
                sys.stdout.flush()



        elif command == 'g':
            display_graph()

        else:
            print 'Error: ' + 'Wrong input please try again'


if __name__ == '__main__':
    main()

