import subprocess


def bson_to_json(input_file, output_file):
    output = open(output_file, "w")
    subprocess.Popen(["bsondump", input_file], stdout=output).wait()
    output.close()
