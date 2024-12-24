import mysql.connector


def convert_to_blob(file_path: str):
    with open(file_path, "rb") as f:
        binary_data = f.read()
    return binary_data


def insert():
    connection = mysql.connector.connect(
        host="103.178.57.34",
        user="root",
        passwd="KangoShyVpn500",
        database="mv"
    )
    cursor = connection.cursor()
    try:
        for id in range(7, 21):
            sql_insert = """ update mv_manage set cover_image = %s where id = %s """
            blob = convert_to_blob(f"/Users/kangoshayne/Downloads/工作下载目录/学习资料/{id}.jpg")
            update_tuple = (blob, id)
            cursor.execute(sql_insert, update_tuple)
            connection.commit()
    except Exception as e:
        print(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == '__main__':
    insert()
