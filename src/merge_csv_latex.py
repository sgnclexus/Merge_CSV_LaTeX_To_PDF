import pandas as pd
import subprocess
import platform
import time


MODALIDAD = {
    "prog_est":[9,8,7,6,5,4,3,2,1]
    ,"prog_description":[
                        "SG"
                        ,"ST"
                        ,"TE"
                        ,"BG (PA)"
                        ,"BG (PS)"
                        ,"BG (P2A)"
                        ,"BT"
                        ,"PT"
                        ,"CPT"
    ]
}

# Function to convert a string to camel case
def to_camel_case(text):
    """
    Function to change to camel case and standard the input text
    """
    words = text.split()
    # Capitalize the first letter of each word except the first one, and then join them
    return ' '.join(word.capitalize() for word in words)


def grettings_generator():
    """
    Function to generate a PDF File (Greeting Document) from LaTeX using python to get info from csv
    """

    dfSchools = pd.read_csv("data\Schools.csv", sep=",", encoding="utf-8")
    dfSchools["dir_nom"] = dfSchools["dir_nom"].apply(to_camel_case)
    dfSchools["CCT_nom"] = dfSchools["CCT_nom"].apply(to_camel_case)

    for index, row in dfSchools.iterrows():
        
        with open(f"template\Grettings\Greeting.tex", "r", encoding="utf-8") as template_file:
            latex_content = template_file.read()

        latex_content = latex_content.replace("{{Principal}}", row["dir_nom"])
        latex_content = latex_content.replace("{{School}}", row["CCT_nom"])

        with open("output.tex", "w", encoding="utf-8") as output_file:
            output_file.write(latex_content)

        pdf_filename = f"output\Grettings\{row["CCT"]}_Agradecimiento.pdf"

        subprocess.run(["pdflatex", "-jobname="+pdf_filename.replace(".pdf",""), "output.tex"])

        # Clean up auxiliary files (optional)
        # Detect the OS and use the appropriate file deletion command
        if platform.system() == "Windows":
            print(f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\{pdf_filename.replace(".pdf","")}.log")
            subprocess.run(["del", f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\{pdf_filename.replace(".pdf","")}.log", f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\{pdf_filename.replace(".pdf","")}.aux"], shell=True)  # Windows command
            subprocess.run(["del", f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\output.tex"], shell=True)
        else:
            subprocess.run(["rm", f"output\\Grettings\\{pdf_filename.replace(".pdf","")}.log", f"output\\Grettings\\{pdf_filename}.aux"])  # Unix/Linux command
            subprocess.run(["rm", "output.tex"])

            

def principalAccess_generator():
    """
    Function to generate a PDF File (Login Access Document) from LaTeX using python to get info from csv
    """    

    dfSchools = pd.read_csv(f"data\Schools.csv", sep=",", encoding="utf-8")
    dfSchools["dir_nom"] = dfSchools["dir_nom"].apply(to_camel_case)
    dfSchools["CCT_nom"] = dfSchools["CCT_nom"].apply(to_camel_case)

    for index, row in dfSchools.iterrows():
        
        with open(f"template\PrincipalAccess\principalAccess.tex", "r", encoding="utf-8") as template_file:
            latex_content = template_file.read()

        latex_content = latex_content.replace("{{Principal}}", row["dir_nom"])
        latex_content = latex_content.replace("{{School}}", row["CCT_nom"])
        latex_content = latex_content.replace("{{CCTID}}", row["CCT"])
        latex_content = latex_content.replace("{{User}}", str(row["Sch_login"]))
        latex_content = latex_content.replace("{{Password}}", str(row["Sch_password"]))

        with open("output.tex", "w", encoding="utf-8") as output_file:
            output_file.write(latex_content)

        pdf_filename = f"output\PrincipalAccess\{row["CCT"]}_DirectorAcceso.pdf"

        subprocess.run(["pdflatex", "-jobname="+pdf_filename.replace(".pdf",""), "output.tex"])

        # Clean up auxiliary files (optional)
        # Detect the OS and use the appropriate file deletion command
        if platform.system() == "Windows":
            print(f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\{pdf_filename.replace(".pdf","")}.log")
            subprocess.run(["del", f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\{pdf_filename.replace(".pdf","")}.log", f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\{pdf_filename.replace(".pdf","")}.aux"], shell=True)  # Windows command
            subprocess.run(["del", f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\output.tex"], shell=True)
        else:
            subprocess.run(["rm", f"output\\Grettings\\{pdf_filename.replace(".pdf","")}.log", f"output\\Grettings\\{pdf_filename}.aux"])  # Unix/Linux command
            subprocess.run(["rm", "output.tex"])



def studentAccess_generator():
    """
    Function to generate a PDF File (Student Login Access Document) from LaTeX using python to get info from csv
    """

    cols = ["Sch_no", "CCT", "CCT_nom"]
    dfStudent = pd.read_csv(f"data\Students.csv", sep=",", encoding="utf-8")
    dfSchools = pd.read_csv(f"data\Schools.csv", sep=",", encoding="utf-8", usecols=cols)
    dfType = pd.DataFrame(MODALIDAD)    

    
    dfStudentSchool = dfStudent.merge(dfSchools, how="inner", left_on=["Sch_no"], right_on=["Sch_no"])    
    dfStudentSchoolType = dfStudentSchool.merge(dfType, how="inner", left_on=["prog_est"], right_on=["prog_est"])    

    dfStudentSchoolType["alu_nom"] = dfStudentSchoolType["alu_nom"].apply(to_camel_case)
    dfStudentSchoolType["CCT_nom"] = dfStudentSchoolType["CCT_nom"].apply(to_camel_case)

    for index, row in dfStudentSchoolType.iterrows():
        
        with open(f"template\\UserAccessSAI\\userAccess.tex", "r", encoding="utf-8") as template_file:
            latex_content = template_file.read()

        latex_content = latex_content.replace("{{LineID}}", str(row["linea_no"]))
        latex_content = latex_content.replace("{{Student}}", row["alu_nom"])
        latex_content = latex_content.replace("{{School}}", row["CCT_nom"])
        latex_content = latex_content.replace("{{CCTID}}", row["CCT"])
        latex_content = latex_content.replace("{{Type}}", row["prog_description"])
        latex_content = latex_content.replace("{{User}}", str(row["id_sai"]))
        latex_content = latex_content.replace("{{Password}}", str(row["passw_sai"]))

        with open("output.tex", "w", encoding="utf-8") as output_file:
            output_file.write(latex_content)

        pdf_filename = f"output\\UserAccessSAI\\{row["CCT"] + "_" + str(row["id_sai"])}_UsuarioAcceso.pdf"

        subprocess.run(["pdflatex", "-jobname="+pdf_filename.replace(".pdf",""), "output.tex"])

        # Clean up auxiliary files (optional)
        # Detect the OS and use the appropriate file deletion command
        if platform.system() == "Windows":
            print(f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\{pdf_filename.replace(".pdf","")}.log")
            subprocess.run(["del", f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\{pdf_filename.replace(".pdf","")}.log", f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\{pdf_filename.replace(".pdf","")}.aux"], shell=True)  # Windows command
            subprocess.run(["del", f"C:\\Users\\cesar.castillo\\CC_Ceneval\\Desarrollo\\MergeReports\\output.tex"], shell=True)
        else:
            subprocess.run(["rm", f"output\\Grettings\\{pdf_filename.replace(".pdf","")}.log", f"output\\Grettings\\{pdf_filename}.aux"])  # Unix/Linux command
            subprocess.run(["rm", "output.tex"])


            

if __name__ == "__main__":

    start_time = time.strftime("%H:%M:%S", time.localtime())

    print("Begin Task : ", start_time)

    grettings_generator()    
    studentAccess_generator()


    end_time = time.strftime("%H:%M:%S", time.localtime())

    print("End Task : ", end_time)
