import re
import json
import os
import shutil
from mdutils.mdutils import MdUtils
from mdutils import Html
import sys
import subprocess

# Home Directory of Script eg. /root/Pi-Hole
root_directory = dir_path = os.path.dirname(os.path.realpath(__file__))
whitelist = {}

# Command to Fetch Whitelist from API_Dict
white_command = " ".join(
    [
        "sqlite3",
        '"/etc/pihole/gravity.db"',
        '"SELECT',
        'domain,comment,\\"group\\".name,\\"group\\".description',
        "FROM",
        "domainlist",
        "INNER",
        "JOIN",
        "domainlist_by_group",
        "ON",
        "domainlist_by_group.domainlist_id=domainlist.id",
        "INNER",
        "JOIN",
        '\\"group\\"',
        "ON",
        '\\"group\\".id=domainlist_by_group.group_id',
        "WHERE",
        'domainlist.type=0"',
    ]
)

def findOccurrences(string):
    if string[:-1] == "\|":
        string = Str[: len(string) - 1]
    indexes = []
    indexes = indexes + [x.start() for x in re.finditer("\|", string)] + [len(string)]
    return indexes


def pairwise(l):
    return [(x, y) for x, y in zip(l[:-1], l[1:])]

try: 
    blacks = subprocess.check_output(
        black_command, shell=True, executable="/bin/bash", stderr=subprocess.STDOUT
    )

    print(blacks)
    sys.exit()
    
except subprocess.CalledProcessError as cpe:
    blacks = cpe.output
    print(blacks)
    
"""
# Run Command to Database, Decoding every line
try:
    result = subprocess.check_output(
        white_command, shell=True, executable="/bin/bash", stderr=subprocess.STDOUT
    )

    for line in result.splitlines():
        # Fetch Data by line
        line = str(line.decode()).rstrip().strip()
        pairs = pairwise(findOccurrences(line))

        # From Pair of Intexes - Get strings
        comment = str(line[pairs[0][0] + 1 : pairs[0][1]]).strip()
        group = str(line[pairs[1][0] + 1 : pairs[1][1]]).strip()
        category = str(line[pairs[2][0] + 1 : pairs[2][1]]).strip()
        domain = str(line[0 : pairs[0][0]]).strip()
        
        # Create a Dictionary
        if category not in whitelist.keys():
            if comment.find("-") != -1:
                whitelist[category] = {
                    group: [
                        {
                            "Domain": str(domain).strip(),
                            "Type": str(
                                (comment[0 : comment.index("-") - 1])).strip(),
                            "Comment": str(comment[comment.index("-") + 1 :]).strip(),
                        }
                    ]
                }
            else:
                whitelist[category] = {
                    group: [
                        {"Domain": str(domain).strip(), "Type": str(comment)}
                    ]
                }
        else:
            if group not in whitelist[category].keys():
                if comment.find("-") != -1:
                    whitelist[category][group] = [
                        {
                            "Domain": str(domain).strip(),
                            "Type": str(
                                (comment[0 : comment.index("-") - 1])).strip(),
                            "Comment": str(comment[comment.index("-") + 1 :]).strip(),
                        }
                    ]
                else:
                    whitelist[category][group] = [
                        {
                            "Domain": str(domain).strip(),
                            "Type": str(comment),
                        }
                    ]
            else:
                if comment.find("-") != -1:
                    whitelist[category][group].append(
                        {
                            "Domain": str(domain).strip(),
                            "Type": str(
                                ((comment[0 : comment.index("-") - 1]))).strip(),
                            "Comment": str(comment[comment.index("-") + 1 :]).strip(),
                        }
                    )
                else:
                    whitelist[category][group].append(
                        {
                            "Domain": str(domain).strip(),
                            "Type": str(comment),
                        }
                    )

except subprocess.CalledProcessError as cpe:
    result = cpe.output

# print(json.dumps(whitelist["Hardware Manufacturers"]["Apple"], sort_keys=False, indent=4))
# sys.exit()

# Reset the Structure before re-creating
shutil.rmtree(os.path.join(root_directory, "Whitelist"), ignore_errors=True)


# Create & Populate the Folder Structure based on Data
def populate_structure(category, subcategories):
    path = os.path.join(root_directory, "Whitelist", category)
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            for sub in subcategories:
                if not os.path.exists(os.path.join(path, sub)):
                    os.makedirs(os.path.join(path, sub))
    except OSError:
        pass


for k, v in whitelist.items():
    populate_structure(k, list(whitelist[k].keys()))

# Populate the Categories inside the README.md
def Populate_Category(mdFile, Title, data):
    for k, v in data.items():
        for x in v.keys():
            mdFile.new_header(
                level=2, title=f"{Title} - {x}", add_table_of_contents="n"
            )
            mdFile.insert_code(str("\n".join(v[x])).strip(), language="html")
            mdFile.write("  \n\n")
            mdFile.write("<br>\n")


translations = {
    "Root Domains": {
        "Priority" : 1,
        "Translation": "Root Domains"
    },
    "Domain": {
        "Priority": 2,
        "Translation": "Domain"
    },
    "Verified Domains": {
        "Priority" : 3,
        "Translation": "Verified Domains"
    },
    "Media Delivery": {
        "Priority": 4,
        "Translation": "Media Delivery"
    },
    "Software Delivery": {
        "Priority": 5,
        "Translation": "Software Delivery"
    },
    "Authentication": {
        "Priority": 6,
        "Translation": "Authentication"  
    },
    "CSS": {
        "Priority" : 7, 
        "Translation" : "Cascading Style Sheets (CSS)"
    },
    "API": {
        "Priority" : 8, 
        "Translation" : "Application Programming Interface (API)"
    },
    "CDN": {
        "Priority" : 9, 
        "Translation" : "Content Delivery Network (CDN)"
    },
    "OCSP": {
        "Priority" : 10, 
        "Translation" : "Online Certificate Status Protocol (OCSPs)"
    },
    "NTP": {
        "Priority" : 11, 
        "Translation" : "Network Time Protocol Servers (NTPs)"
    },
    "OAuth": {
        "Priority" : 12, 
        "Translation" : "Open Authorization Standard (OAuth)"
    },
    "DNS": {
        "Priority" : 13, 
        "Translation" : "Domain Name Systems (DNS)"
    },
}

# Translate the Type from Pihole's Comment Abbreviation to a "Presentable" Term
def translate(abbreviation):
    if abbreviation in translations.keys():
        return translations[abbreviation]["Translation"]
    else:
        return abbreviation

# Remove Duplicates from Lists
def remove_duplicates(l):
    return list(set(l))

# Create Files
def create_file(Title, Static_Types, Non_Types):
    mdFile = MdUtils(file_name="README")
    mdFile.write('<h1 align="center">{}</h1>'.format(str(Title).strip()))
    mdFile.write("  \n\n")
    
    # Static Types
    existence = []
    for typ3 in Static_Types.keys():
        if typ3 in translations.keys():
            if translations[typ3]["Priority"] not in existence:
                existence.append(int(translations[typ3]["Priority"]))
    
    for num in sorted(existence):
        print([value["Tr"] for key, value in translations.items() if value["Priority"] == num])
    
    """
    mdFile.new_header(level=2, title=str(translate([key for key, value in translations.items() if value["Priority"] == num])), add_table_of_contents="n")
    mdFile.insert_code(str("\n".join([1,2,3])).strip(), language="html")
    mdFile.write("  \n\n")
    """
    
    """
    # Non Static Types
    if not Non_Types:
        mdFile.write("<br>\n")
        for k,v in Non_Types.keys():
            Populate_Category(mdFile, translate(k), v)
        # Populate_Category(mdFile, "Content Delivery Networks (CDN)", CDN_Dict)
             
    mdFile.create_md_file()
    """

# API - Application Programming Interface (APIs)
# Specialized APIs that cover a purpose
API_Dict = {}

# Core APIs - Application Programming Interface (APIs)
# Any API that is essential for the core program/website/application and not have a specific purpose that I can find.
API = []

# CDN - Content Delivery Network (CDNs)
CDN_Dict = {}

# CDNs
CDN = []

# Static Types
Static_Types = {}
# 1. Root Domains - The home domains, the root of any domain.
# 2. Verified Domains - Domains that belong to the Application/Website/Program that might have a specific purpose or be subpages.
# These are by majority static pages and urls rather than dynamic that serve some type of content or purpose.

# 3. CSS - Static Assets as interpreted by Pi-Hole Comments
# 4. Media Delivery - Anything that serves content - Videos, Pictures, Sound, Thumbnails, Files, Assets etc.
# 5. Software Delivery - Application Updates, Download Software, Firmware Updates
# 6. Authentication


Non_Types = {}

# Category
for x in whitelist.keys():
    # Group 
    for y in whitelist[x].keys():
        # Domain
        for z in whitelist[x][y]:
            
            # Static Types (No Comment just type)
            
            # Must have no Comment (so no additional specific purpose)
            if "Comment" not in z.keys():
                # Create Type
                if z["Type"] not in Static_Types.keys() and len(z["Type"]) > 0:
                    Static_Types[z["Type"]] = [z["Domain"]]
                    continue    
                
                elif z["Type"] in Static_Types.keys():
                    Static_Types[z["Type"]].append(z["Domain"])
                    continue
            
            else:
                
                # Non-Static Types
                if z["Type"] not in Non_Types.keys():
                    # If type doesn't exist
                    Non_Types[z["Type"]] = {z["Comment"] : [[z["Domain"]]]}
                    continue
                elif z["Type"] in Non_Types.keys():
                    if z["Comment"] not in Non_Types[z["Type"]].keys() and len(z["Comment"]) > 0:
                        # if SubType (Comment) doesn't exist
                        Non_Types[z["Type"]][z["Comment"]] = [z["Domain"]]
                        continue    
                else:
                    # if exists just append
                    Non_Types[z["Type"]][z["Comment"]].append(z["Domain"])
                    continue
               
        Fpath = os.path.join(root_directory, "Whitelist", str(x), str(y))
        if os.path.exists(Fpath):
            os.chdir(Fpath)
            create_file(y,Static_Types,Non_Types)
            # Clear Dictionaries
            Static_Types.clear()
            Non_Types.clear()
            
"""
# Push Changes to Github
from git import Repo

repo = Repo(root_directory)  # if repo is CWD just do '.'
repo.git.add("-A")
repo.git.commit("-m", "Automated Push")
origin = repo.remote(name="origin")
origin.pull()
origin.push()

"""
