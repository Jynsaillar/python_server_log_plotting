import mysql.connector


def querydatabase(dbparams, verbose, arglist=[]):

    '''
    dbparams is a tuple containing 4 elements:
    db user, db password, db hostname, db name.
    arglist should be a list where the first element is the query
    and the second element is a tuple of placeholder values.
    E.g.: arglist = [
        'SELECT * FROM table WHERE %s = 0 OR %s = 1;', ('apples', 'bananas')]
    '''
    query = arglist[0]
    results = []

    try:
        cnx = mysql.connector.connect(user=dbparams[0], password=dbparams[1],
                                      host=dbparams[2], database=dbparams[3])

        cursor = cnx.cursor(buffered=True)

        if len(arglist[1]) == 0:
            cursor.execute(query)
        else:
            cursor.execute(*arglist)
        results = cursor.fetchall()
        if verbose:
            print("Successfully fetched <all> from:\n{}".format(query))

    except mysql.connector.Error as error:
        print("Failed to execute query: {}".format(error))
        cnx.rollback()
    finally:
        cursor.close()
        if(cnx.is_connected()):
            cnx.close()
        if verbose:
            print("MySQL connection closed.")
    return results


def queryservernames():

    getservernames = '''
    SELECT DISTINCT name FROM servermonitor;
    '''
    return [getservernames, ()]


def queryserverlog(server_name, date_blob):

    _, _, date_from, date_to = date_blob
    getserverlog = '''
    SELECT
        DATE_FORMAT(
            DATE_ADD(scrape_date, INTERVAL 30 MINUTE),
            '%Y-%m-%d %H:00:00') as 'date',
        MIN(user_count) as 'least users',
        CAST(ROUND(AVG(user_count)) AS INT) 'average users',
        MAX(user_count) as 'most users'
    FROM
        servermonitor
    WHERE
        name = %s AND scrape_date BETWEEN %s AND %s
    GROUP BY
        DATE(scrape_date),
        HOUR(scrape_date)
    ORDER BY
        DATE(scrape_date),
        HOUR(scrape_date);
    '''
    return [getserverlog, (server_name, date_from, date_to)]


def querymaxplayers(date_blob):

    _, _, date_from, date_to = date_blob
    getmaxplayers = '''
    SELECT
        MAX(user_count)
    FROM
        servermonitor
    WHERE
        scrape_date BETWEEN %s and %s;
    '''
    return [getmaxplayers, (date_from, date_to)]


def getservernames(dbparams, verbose):
    return querydatabase(dbparams, verbose,
                         arglist=queryservernames())


def getserverlog(dbparams, verbose, date_blob, server_name):
    return querydatabase(dbparams, verbose,
                         arglist=queryserverlog(server_name, date_blob))


def getmaxplayers(dbparams, verbose, date_blob):
    return querydatabase(dbparams, verbose,
                         arglist=querymaxplayers(date_blob))[0][0]
