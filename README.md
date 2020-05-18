# python Semester Project


##### importing required modules
pip install --no-cache-dir tabula-py numpy requests pandas


#### For  windows 10 brugere

 * If you don’t have it already, install Java
 * Try to run example code (replace the appropriate PDF file name).
 * If there’s a FileNotFoundError when it calls read_pdf(), and when you type java on command line it says 'java' is not recognized as an internal or external command, operable program or batch file, you should set PATH environment variable to point to the Java directory.
 * Find the main Java folder like jre... or jdk.... On Windows 10 it was under C:\Program Files\Java
 * On Windows 10: Control Panel -> System and Security -> System -> Advanced System Settings -> Environment Variables -> Select PATH –> Edit
 * Add the bin folder like C:\Program Files\Java\jre1.8.0_144\bin, hit OK a bunch of times.
 * On command line, java should now print a list of options, and tabula.read_pdf() should run.

##### Eksempel tabula - test.pdf skal være en gyldig pdf fil i samme folder
    import tabula

    tabula.convert_into("test.pdf", "output.csv", output_format="csv", pages='all')
