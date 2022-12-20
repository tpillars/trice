from re import match
import csv


def get_file_info(my_bucket):
    """Returns s3 bucket name and prefix (date) in form of .csv"""
    format = "^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[a-z]"
    projectlist = []
    header = ["date", "project"]
    with open("results/s3-file-info.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for my_bucket_object in my_bucket.objects.all():
            mystring = str(my_bucket_object)
            filepath = mystring.split(",")[1]
            all_results = filepath.split("/")
            for result in all_results:
                if match(format, result):
                    directory = result.split(".")[0]
                    if directory in projectlist:
                        pass
                    else:
                        projectlist.append(directory)
        for directory in projectlist:
            project = directory[8:]
            date = directory[:7]
            writer.writerow([date, project])
    file.close()
