def get_warnings(connection):
    warnings = connection.show_warnings()
    if warnings:
        print('warnings:', warnings)


def get_script_from_file(filename):
    f = open(filename, 'r')
    script = f.read()
    f.close()
    return script


def get_report(mysql, script):
    conn = mysql.connect()
    get_warnings(conn)
    cursor = conn.cursor()
    cursor.execute(script)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    # print('report results:', results)
    return results
