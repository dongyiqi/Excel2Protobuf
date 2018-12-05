#Convert Excel file to Protobuf file by Python script

HOW TO USE

# parameters
# -i --input_path input folder which contains excel files to convert.
#       This script converts all excel file from that folder
# -d --data_out folder where serialized binary protobuf file exported
# -s --csharp_out folder where auto generated C# script file(from protoc.exe) exported
# -c --cpp_out folder where auto generated C++ script file(from protoc.exe) exported


referenced from https://github.com/jameyli/tnt
what i do
1.update to python3 from python2
2.update to protobuf3 from protobuf2
3.refactor the classes and method(almost rewrite) to archive a better easier readable code
