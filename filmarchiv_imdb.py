#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from colorama import Fore, Back, Style
import re
import fileinput
import glob
import shutil
from imdb import IMDb, helpers


ia = IMDb()
#ia = IMDb('sql', uri='sqlite:///home/th/imdb_2012-10.db')

#print ia.search_movie('Adventureland (2009)')
#print ia.search_movie('500 days of summe')


root = r"/mnt/Filmarchiv".rstrip("/")
root_SrcFolder = "Archiv".strip("/")
root_DestFolder = "Sortierung".strip("/")  #ACHTUNG!! Ordner wird komplett geleert!

source = os.path.join(root, root_SrcFolder)
destination = os.path.join(root, root_DestFolder)

actor_ids =[
            "0000093", "0000098", "0000113", "0000115", "0000123", "0000126", "0000128", "0000129",
            "0000136", "0000138", "0000139", "0000142", "0000148", "0000149", "0000151", "0000152",
            "0000154", "0000158", "0000163", "0000168", "0000169", "0000173", "0000193", "0000199",
            "0000201", "0000206", "0000210", "0000226", "0000228", "0000235", "0000237", "0000243",
            "0000244", "0000245", "0000246", "0000250", "0000288", "0000354", "0000432", "0000553",
            "0000569", "0000932", "0001191", "0001293", "0001352", "0001401", "0001774", "0004695",
            "0004874", "0005028", "0005132", "0005227", "0005346", "0005476", "0124930", "0416673",
            "0424060", "0461136", "0479471", "0817881", "0908094", "0000134"
            ]
actor_objects = list()

genres = ["Action", "Animation", "Comedy", "Drama", "Family", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]


def getActorObjects():
    for id in actor_ids:
        obj = ia.get_person(id)
        actor_objects.append(obj)
        print id + "\t" + obj['name']


def findImdbIDfromName(path):
    search = ia.search_movie(os.path.basename(path))
    if len(search) == 0:
        return 0
    else:
        id = ia.get_imdbID(search[0])
        return id


def findImdbIDfromNFO(path):
    nfo = None
    id  = 0
    #find NFO
    for file in os.listdir(path):
        if file.endswith('.nfo'):
            nfo = os.path.join(path, file)
    if not nfo:
        return -1
    #parse NFO for imdb link
    for line in fileinput.input(nfo):
        m = re.search(r".*www.imdb.com.title.tt(\d{7})", line)
        if (m is not None):
            id = m.group(1)
            break
    fileinput.close()
    if not id:
        return 0
    return id

def findImdbIDfromSFV(path):
    sfvfilepath = None
    id  = 0
    for file in os.listdir(path):
        if file.endswith('.sfv'):
            sfvfilepath = os.path.join(path, file)
    if not sfvfilepath:
        return -1
    #parse NFO for IMDb link
    for line in fileinput.input(sfvfilepath):
        m = re.search(r"; http...*www.imdb.com.title.tt(\d{7})", line)
        if (m is not None):
            id = m.group(1)
            break
    fileinput.close()
    if not id:
        return 0
    return id

def findImdbIDfromURL(path):
    urlfilepath = None
    id = 0
    for file in os.listdir(path):
        if file.endswith('.url'):
            urlfilepath = os.path.join(path, file)
    if not urlfilepath:
        return -1
    #parse NFO for IMDb link
    for line in fileinput.input(urlfilepath):
        m = re.search(r"URL.http...www.imdb.*.tt(\d{7})", line)
        if (m is not None):
            id = m.group(1)
            break
    fileinput.close()
    if not id:
        return 0
    return id

def writeIDtoSFV(folderpath,id):
    files = glob.glob(folderpath + os.sep + "*.sfv")
    if len(files)!=1:
        print Fore.RED + "WARNING nicht eine einzelne SFV " + folderpath + Fore.RESET
        return 0
    sfvfilepath = files[0]
    writelist = []
    writelist.append('\n')
    writelist.append(';/-------------------------------------\n')
    writelist.append('; http://www.imdb.com/title/tt'+id+'/\n')
    writelist.append(';\\-------------------------------------\n\n')
    for line in fileinput.input(sfvfilepath):
        if not line.startswith(';') and not line.strip()=='':
            if "00000" in line:
                print Fore.RED + "WARNING SFV ungültige CRC (00000000) " + sfvfilepath + Fore.RESET
            writelist.append(line.replace('\r\n','\n'))
    fileinput.close()
    writelist.append('\n')
    try:
        f = open(sfvfilepath, "w")
        f.writelines(writelist)
        f.close()
        print Fore.GREEN + "SFV erfolgreich bearbeitet " + sfvfilepath + Fore.RESET
    except IOError:
        print Fore.RED + "WARNING SFV nicht schreibbar " + sfvfilepath + Fore.RESET
        pass


def writeIDtoURLfile(folderpath,id):
    files = glob.glob(folderpath + os.sep + "*.url")
    if len(files) != 0:
        print Fore.RED + "eine URL Datei ist bereits vorhanden: " + folderpath + Fore.RESET
        return 0

    urlfilepath = folderpath + os.sep + os.path.basename(folderpath) + ".url"
    try:
        f = open(urlfilepath, "w")
        f.write('[InternetShortcut]\nURL=http://www.imdb.de/title/tt' + id + '/')
        f.close()
        print Fore.GREEN + "URL erfolgreich erstellt " + urlfilepath + Fore.RESET
    except IOError:
        print Fore.RED + "WARNING URL nicht schreibbar " + urlfilepath + Fore.RESET
        pass


def writeActorIDtoURLfile(destination, actor):
    urlfilepath = destination + os.sep + actor['name'] + ".url"
    if os.path.exists(urlfilepath):
        return 0
    try:
        f = open(urlfilepath, "w")
        f.write('[InternetShortcut]\nURL=http://www.imdb.de/name/nm' + actor.getID() + '/')
        f.close()
        print Fore.GREEN + "URL erfolgreich erstellt " + urlfilepath + Fore.RESET
    except IOError:
        print Fore.RED + "WARNING URL nicht schreibbar " + urlfilepath + Fore.RESET
        pass






def processFolder(folder):
    print "\n\n" + "═"*80
    print "Folder Name:   " + os.path.basename(folder)
    #1. IMDb ID ausder selbst URL Datei auslesen
    id = findImdbIDfromURL(folder)
    if (id<=0):
        #2. Wenn in der URL Datei keine ID zu finden war: Probiere die NFO und bei Erfolg schreibe die URL Datei neu
        print Fore.YELLOW + 'ID nicht in URL Datei gefunden. überprüfe NFO...' + Fore.RESET
        id = findImdbIDfromNFO(folder)
        if (id > 0):
            print Fore.GREEN + "NFO enthält ID " + id + Fore.RESET
            writeIDtoURLfile(folder,id)
    if (id<=0):
        #3. War auch aus der NFO nichts zu holen, mach einen Vorschlag und frage
        print Fore.RED + 'ID muss manuell oder nach Namen nachgetragen werden!' + Fore.RESET
        maybeid = findImdbIDfromName(folder)
        if maybeid:
            print "Vorschlag:   " + maybeid + " http://www.imdb.de/title/tt" + maybeid
            germanaka = helpers.getAKAsInLanguage(ia.get_movie(maybeid),"German")
            if len(germanaka) > 0:
                print "IMDb Deutsch:  " + germanaka[0]
            print ia.get_movie(maybeid).summary()
            print ""
        else:
            print Fore.CYAN + "kein Vorschlag gefunden" + Fore.RESET
        id = raw_input('Bitte IMDb ID oder Link eingeben, "v" für Vorschlag, "" für Überspringen: ')
        if id == "v": id = maybeid
        m = re.search(r".*imdb.*tt(\d*)", id)
        if (m is not None):
            id = m.group(1)
        if len(id) != 7:
            print Fore.RED + "nicht akzeptierte oder unerwartete ID" + Fore.RESET
            return None
        writeIDtoURLfile(folder,id)
    movie = ia.get_movie(id)
    print "IMDb Title:    " + movie['long imdb title']
    germanaka = helpers.getAKAsInLanguage(movie,"German")
    if len(germanaka) > 0:
        print "IMDb Deutsch:  " + germanaka[0] + " (" + str(movie['year']) + ")"
    print "IMDb ID:       " + str(id)
    print "\n" + Fore.BLACK + Style.BRIGHT + movie.summary() + Style.RESET_ALL + "\n"
    return movie

def hardlinkFolder(src, dest):
    os.mkdir(dest)
    for filename in os.listdir(src):
        os.link(src + os.sep + filename, dest + os.sep + filename)

def cleanDestination(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    print Fore.YELLOW + 'Zielverzeichnis geleert...' + Fore.RESET


def LinkMovieByRules(src, dest, movie):

    destinationBase = root + os.sep + root_DestFolder
    movieFolderTitle = os.path.basename(src)
    #print movie.keys()
    #print "IMDb Votes:\t" + str(movie['votes'])
    #print movie.summary()
    #germanaka = helpers.getAKAsInLanguage(movie,"German")
    #if len(germanaka) > 0:
    #    print "IMDb Deutsch:  " + germanaka[0]
    #print "IMDb Title:\t" + movie['title']
    #print "IMDb Year:\t" + str(movie['year'])
    #print "IMDb Rating:\t" + str(movie['rating'])
    #print movie['cast'][0:3]

    if (True):
        destSubdir = destinationBase + os.sep + "A-Z"
        if not os.path.exists(destSubdir):
            os.makedirs(destSubdir)
        hardlinkFolder(src, destSubdir + os.sep + movieFolderTitle)

    if (True):
        if movie['year'] <= 1970:
            destSubdir = destinationBase + os.sep + "Jahr" + os.sep + "1900-1970"
            if not os.path.exists(destSubdir):
                os.makedirs(destSubdir)
            hardlinkFolder(src, destSubdir + os.sep + movieFolderTitle)
            print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET
        if movie['year'] in range(1971, 1991):
            destSubdir = destinationBase + os.sep + "Jahr" + os.sep + "1971-1990"
            if not os.path.exists(destSubdir):
                os.makedirs(destSubdir)
            hardlinkFolder(src, destSubdir + os.sep + movieFolderTitle)
            print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET
        for year in range(1991, 2020):
            if movie['year'] == year:
                destSubdir = destinationBase + os.sep + "Jahr" + os.sep + str(year)
                if not os.path.exists(destSubdir):
                    os.makedirs(destSubdir)
                hardlinkFolder(src, destSubdir + os.sep + movieFolderTitle)
                print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET

    if (True):
        try:
            for genre in genres:
                if genre in movie['genres']:
                    destSubdir = destinationBase + os.sep + "Genre" + os.sep + genre
                    if not os.path.exists(destSubdir):
                        os.makedirs(destSubdir)
                    hardlinkFolder(src, destSubdir + os.sep + movieFolderTitle)
                    print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET
        except KeyError, e:
            print Fore.MAGENTA + "keine Genres verfügbar: " + str(e) + Fore.RESET

    if (True):
        try:
            destSubdir = destinationBase + os.sep + "IMDb Bewertung"
            if not os.path.exists(destSubdir):
                os.makedirs(destSubdir)
            hardlinkFolder(src, destSubdir + os.sep + "(" + str(movie['rating']) + ")  " + movieFolderTitle)
            #print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET
        except KeyError, e:
            print Fore.MAGENTA + "kein Rating gefunden: " + str(e) + Fore.RESET

        try:
            destSubdir = destinationBase + os.sep + "IMDb Votes"
            if not os.path.exists(destSubdir):
                os.makedirs(destSubdir)
            votesstr = str(movie['votes'])
            votesstr = '0'*(6 - len(votesstr)) + votesstr
            hardlinkFolder(src, destSubdir + os.sep + votesstr + " - " + movieFolderTitle)
            #print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET
        except KeyError, e:
            print Fore.MAGENTA + "keine Votes gefunden: " + str(e) + Fore.RESET


    if (True):
        try:
            if movie['countries'][0] == "Germany" and movie['languages'][0] == "German":
                destSubdir = destinationBase + os.sep + "Land" + os.sep + "Deutschland"
                if not os.path.exists(destSubdir):
                    os.makedirs(destSubdir)
                hardlinkFolder(src, destSubdir + os.sep + movieFolderTitle)
                print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET
            elif movie['countries'][0] == "France" and movie['languages'][0] == "French":
                destSubdir = destinationBase + os.sep + "Land" + os.sep + "Frankreich"
                if not os.path.exists(destSubdir):
                    os.makedirs(destSubdir)
                hardlinkFolder(src, destSubdir + os.sep + movieFolderTitle)
                print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET
            elif (movie['countries'][0] == "Denmark" and movie['languages'][0] == "Danish") or\
                 (movie['countries'][0] == "Norway" and movie['languages'][0] == "Norwegian"):
                destSubdir = destinationBase + os.sep + "Land" + os.sep + "Skandinavien"
                if not os.path.exists(destSubdir):
                    os.makedirs(destSubdir)
                hardlinkFolder(src, destSubdir + os.sep + movieFolderTitle)
                print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET
        except KeyError, e:
            print Fore.MAGENTA + "keine Languages gefunden: " + str(e) + Fore.RESET
        except IndexError, e:
            print Fore.MAGENTA + "keine Languages gefunden: " + str(e) + Fore.RESET


    if (True):
        for actor in actor_objects:
            if actor in movie:
                destSubdir = destinationBase + os.sep + "Schauspieler" + os.sep + actor['name']
                if not os.path.exists(destSubdir):
                    os.makedirs(destSubdir)
                    writeActorIDtoURLfile(destSubdir, actor)
                try:
                    hardlinkFolder(src, destSubdir + os.sep + movieFolderTitle)
                    print Fore.YELLOW + "hardlink --> " + destSubdir + Fore.RESET
                except UnicodeDecodeError, e:
                    print Fore.RED + "IMDbPY Error(?) " + str(e) + Fore.RESET





cleanDestination(destination)
#getActorObjects()
for sourceSubFolder in sorted(glob.glob(source + os.sep + "*")):
    movie = processFolder(sourceSubFolder)

    #TODO auslagern
    m = re.search(r".* \(\d{4}\)$", sourceSubFolder)
    if (m is None):
        new = raw_input('Ordner hat keinen gültigen Namen. Bitte neune Name eingeben oder mit "" belassen: ')
        if new != "":
            newSubFolder = os.path.dirname(sourceSubFolder) + os.sep + new
            try:
                os.rename(sourceSubFolder, newSubFolder)
                print Fore.CYAN + "erfolgreich umbenannt: " + sourceSubFolder + " --> " + newSubFolder + Fore.RESET
                sourceSubFolder = newSubFolder
            except OSError:
                print Fore.RED + "Fehler beim Umbenennen: " + sourceSubFolder + " --> " + newSubFolder + Fore.RESET
                pass

    if movie: LinkMovieByRules(sourceSubFolder, destination, movie)
