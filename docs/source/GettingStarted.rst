Getting Started
--------------------------------------------------------------------------------

Ausführen (exportieren) eines Scenarios
================================================================================
Um ein Scenario zu exportieren kann das python script msml.py genutzt werden. Die Optionen können mit "python msml.py -h" angezeigt werden:

suwelack@i61p138:~/git/msmlGit/MSML_Python$ python msml.py -h
Usage: msml.py [options]

Options:
-h, --help show this help message and exit
-f FILE, --file=FILE MSML file
-e EXPORTENGINE, --exporter=EXPORTENGINE
Specify exporter engine; sofa, abaqus or generic
-d DIRECTORY, --directory=DIRECTORY
output directory
-r, --rebuildAlphabet
rebuild alphabet
-n, --nocaching enable/disable caching

Wenn kein exporter angegeben wird, so wird der generic exporter genutzt (alle pipelines werden ausgeführt). Z.B.
python msml.py -f ../Testdata/LiverExample/postProcessingExample.xml

Das script kann auch aus anderen Verzeichnissen ausgeführt werden, z.B. aus dem Verzeichnis wo die Testdaten liegen:
python ../MSML_Python/msml.py -f LiverExample/postProcessingExample.xml
Edit
Erstellen eines Scenarios

Beim Erstellen eines Scenarios orientiert man sich am besten an den bereits verfügbaren Beispielen. Diese sind:
LiverExample/liverExample.xml
LiverExample/liverExampleLinear.xml
LiverExample/postProcessingExample.xml
BunnyExample/bunnyExample.xml
CGALi2vExample/CGALExample.xml
CGALi2vLungs/LungsHighRes.xml

Wichtig (!): Das Verzeichnes, welches im MSML-fiel angegeben wird ist relativ zu dem übergeordneten Verzeichnis, in dem die MSML-Datei liegt!
