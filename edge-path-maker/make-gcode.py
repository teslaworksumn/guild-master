import Edge_Detection
import gcode_postprocessing
import os

scale_factor = 40
imagesDirectory = "edge-path-maker/images/"
gcodeDirectory = "edge-path-maker/gcode/"

def makeGCode(edges, width, height):
    commands = []
    oldpoint = (0,0)
    for edge in edges:
        commands += ["S225"]
        i = 0
        for i in range(0, len(edge) - 2, 2):
            point = edge[i]
            x = point[0]# - oldpoint[0]
            y = point[1]# - oldpoint[1]
            commands += ["G91 G0 " + "X" + str((x - oldpoint[0])/scale_factor) + " " + "Y" + str((y - oldpoint[1])/scale_factor)]
            oldpoint = point
            if(i == 0):
                commands += ["S255"]
        for i in range(len(edge)-2, len(edge)):
            point = edge[i]
            x = point[0]# - oldpoint[0]
            y = point[1]# - oldpoint[1]
            commands += ["G91 G0 " + "X" + str((x - oldpoint[0])/scale_factor) + " " + "Y" + str((y - oldpoint[1])/scale_factor)]
            oldpoint = point
    return commands

def writeToFile(fileName, gcode):
    with open(os.path.join(gcodeDirectory, fileName), "w+") as fin:
        for line in gcode:
            fin.write("%s\n" %line)
        gcodePrepend = gcode_postprocessing.prepend()
        fileData = fin.read()
        fin.seek(0,0)
        fin.write(gcodePrepend.rstrip('\r\n') + '\n' + fileData)

if __name__ == '__main__':
    imgName = input("Image name: ")
    fileName = input("GCode file name: ")
    if (imgName == ""):
        imgName = "tesla_works_logo.png"
        print("No image name given. Using default image")
        if (fileName == ""):
            fileName = "tesla_works_logo.gcode"
            print("no file name given. Using default file name")
    elif (fileName == ""):
        raise ValueError("you must give a file name")
    raw_drawing, width, height = Edge_Detection.prepEdgePainter(imagesDirectory + imgName)
    gcode = makeGCode(raw_drawing, width, height)
    writeToFile(fileName, gcode)