#import required modules
import praw, os, config, pickle, shutil, pathlib
from praw.models import Submission
from praw.models import Comment

#importing configs and PRAW
reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent,
                     username=config.username,
                     password=config.password)

#Functions
def Head_tag(data,num):
    num = str(num)
    data = str(data)
    data = '<h'+ num +'>'+ data + '</h'+num+'>'
    return data

def Span_tag(data,c):
    data = str(data)
    if c == 's':
        classid = 'class = "subreddit"'
    elif c == 'u':
        classid = 'class = "user"'
    elif c == 'c':
        classid = 'class = "numcomments"'
    else:
        None
    data = '<span '+ classid +'>'+ data +' </span>'
    return data

def Anchor_tag(data, source):
    data = str(data)
    data = '<a href="' + data + '" target="_blank">'+ source + '</a>'
    return data

def syncload():
    with open('sync.p', 'rb') as h:
        recent_id = str(pickle.load(h))
        print('Last saved ID:', recent_id)
        return recent_id
        h.close()

def syncdump(submissionid):
    with open('sync.p','wb') as f:
        print('Updating Last saved  Id:', submissionid)
        pickle.dump(submissionid, f)
        f.close()

def newrecent():
    saved = reddit.user.me().saved(limit=1)
    for submission in saved:
        print('Recent id:')
        print(submission.id)
        submissionid = str(submission.id)
        return submissionid

def partialhead(file_name,title, ref_path):
    file_name = str(file_name)
    title = str(title)
    with open(file_name, 'a', encoding="utf-8") as f:
        data = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{0}</title>
    <link href="https://fonts.googleapis.com/css?family=Sniglet|Open+Sans:400,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{1}">
</head>
<body>
    <div class="container">"""
        data = data.format(title, ref_path)
        f.write(data)

def runn(submission):
    #if the submission is a post
    if isinstance(submission, Submission):
            print('Post', submission.id)
            sub = str(submission.subreddit)
            file_name = sub + '.html'
            partialhead(file_name, sub, '../assets/css/style.css')
            with open(file_name, 'a', encoding="utf-8") as h:
                h.write(Head_tag(Span_tag(submission.subreddit_name_prefixed,'s'),1) + "\n")
                submission = newsyncsubmission(submission)
                h.write(submission)

def newsyncsubmission(submission):
    if isinstance(submission, Submission):
        title = Head_tag(submission.title,2)
        author = Span_tag('posted by: u/' + str(submission.author) ,'u')
        num_comments = Span_tag(str(submission.num_comments) + ' comments', 'c')
        submission_url = Anchor_tag(submission.url, '(source)')
        item_num = str(submission.id)
        if(submission.selftext_html != None):
            value = submission.selftext_html
        else:
            value = '<p>NO BODY FOR THE POST</p>'
    elif isinstance(submission, Comment):
        title = Head_tag(submission.link_title,2)
        author = Span_tag('posted by: u/' + str(submission.author) ,'u')
        num_comments = Span_tag(str(submission.num_comments) + ' comments', 'c')
        submission_url = Anchor_tag(submission.permalink, '(source)')
        item_num = str(submission.id)
        if(submission.body_html != None):
            value = submission.body_html
        else:
            value = '<p>NO BODY FOR THE POST</p>'

    new_submission = """<div class="post">
{0}
{1}
{2}
{3}
<button onclick="toggles('{4}')">View full post</button>
<div id="{5}" class="mdwrapper">
{6}
</div>
</div>
    """
    write_submission = new_submission.format(title, author, num_comments, submission_url, item_num, item_num, value)
    print(write_submission)
    return write_submission

def partialfooter(file_name, ssub):
    file_name = str(file_name)
    with open(file_name, 'a', encoding="utf-8") as f:
        l1 = '    <div class="dropdown">'
        l2 = '        <input type="text" id="myInput" onkeyup="filterlist()" placeholder="Search here.." title="Search for subs">'
        l3 = '        <button class= "dropbtn">Subreddits</button>'
        l4 = '        <div class="dropdown-content">'
        l5 = '        <ul class="landinglist" id ="filterlist">'
        lines = [l1,l2,l3,l4,l5]
        f.writelines("%s\n" % l for l in lines)
        for a in ssub:
            print(a)
            with open(a + '.html', 'a', encoding="utf-8") as h:
                h.write('</div>' + '\n')
                h.write('<script src="../assets/js/script.js"></script>' + "\n")
                h.write('</body></html>')
            l6 = '<li>' + Anchor_tag("subs/"+ a + ".html", 'r/' + a)+ '</li>' + "\n"
            f.write(l6)
        l7 = '        </ul>'
        l8 = '</div></div></div>'
        l9 = '<script src="assets/js/script.js"></script>'
        l10 = '</body></html>'
        lines = [l7,l8,l9,l10]
        f.writelines("%s\n" % l for l in lines)

def rerun(submission):
    #check if sub file exists
    new_sub_list = []
    print(submission.subreddit)
    sub = str(submission.subreddit) + ".html"
    if (os.path.isfile(sub)):
        #if file exists then append new submission
        with open(sub, 'r', encoding="utf-8") as f:
            contents = f.readlines()
            new_submission = newsyncsubmission(submission)
            contents.insert(11, new_submission)
        with open(sub, 'w', encoding="utf-8") as f:
            contents = "".join(contents)
            f.write(contents)
    else:
        print('Post saved on new subreddit: creating new file')
        runn(submission)
        new_sub_list.append(str(submission.subreddit))
        print(new_sub_list)
    return new_sub_list

#Paths
#work only if this statement is true #print(reddit.read_only)

#path to this python file
file_path = pathlib.Path(__file__).resolve()
print('The current working directory is:')
print(os.getcwd())

# set save directory
try:
    # see if save directory set in config.py
    config.savedir
    if config.savedir != None:
        Downloads = pathlib.PosixPath(config.savedir)
        parent_path = Downloads
        child_path = parent_path / 'subs'
    else:
        home_path =  pathlib.Path().home()
        Downloads = home_path / Downloads
        parent_path = Downloads / 'Redditsaved'
        child_path = parent_path / 'subs'
except:
    print('Error setting save directory from config.py')

if not os.path.exists(parent_path):
    if not os.path.exists(child_path):
        print('making new path')
        os.makedirs(child_path)

# I dont see the point of this code.
os.chdir(Downloads)
print('Changed the current working directory to:')
print(os.getcwd())

os.chdir(child_path)
print(os.getcwd())

#checking if the program is syncing or for the first time
#if sync id exits
if (os.path.isfile('sync.p')):
    print('Syncing new submissions')
    recent_id = syncload()
    saved = reddit.user.me().saved(limit=1000)
    for submission in saved:
        submission_id = str(submission.id)
        print('Processing new submission with ID:' + submission_id)
        if(recent_id == submission_id):
            #if compare is true break: In perfect sync
            print('No new submissions: Terminating sync')
            break;
        else:
            print('Sync in progress')
            new_subs = rerun(submission)
            print(new_subs)
            for a in new_subs:
                print(a)
                h = open(a+ '.html', 'a', encoding="utf-8")
                h.write('</div>' + '\n')
                h.write('<script src="../assets/js/script.js"></script>' + "\n")
                h.write('</body></html>')
                h.close()

    new_first= newrecent()
    syncdump(new_first)

#If sync.p does not exist, the program is running for the first time
else:
    submission_id = newrecent()
    syncdump(submission_id)
    # generating a listing generator PRAW to get all savd items
    saved = reddit.user.me().saved(limit=1000)
    # counter for total number of saved items
    item_num = 0
    #all sub reddits list
    subs = []
    allsubmissionids =[]

    #landing page header and h1
    with open('Landing.html', 'a', encoding="utf-8") as f:
        partialhead('Landing.html', 'Reddit is saved', 'assets/css/style.css')
        f.write('<h1 class="title">"Reddit is saved"</h1>')

    #looping through all saved items
    for submission in saved:
            item_num += 1
            allsubmissionids.append(str(submission.id))
            if isinstance(submission, Submission):
                print('Post', item_num)
                sub = str(submission.subreddit)
                file_name = sub + '.html'
                with open(file_name, 'a', encoding="utf-8") as h:
                    if sub in subs:
                        print('sub exists, appending')
                    else:
                        #sub files append
                        partialhead(file_name, sub, '../assets/css/style.css')
                        h.write(Head_tag(Span_tag(submission.subreddit_name_prefixed,'s'),1) + "\n")
                        subs.append(sub)
                    h.write('<div class="post">' + '\n')
                    h.write(Head_tag(submission.title,2) + '\n')
                    h.write(Span_tag('posted by: u/' + str(submission.author) ,'u'))
                    h.write(Span_tag(str(submission.num_comments) + ' comments', 'c'))
                    h.write(Anchor_tag(submission.url, '(source)') + '\n')
                    h.write('<button onclick="toggles('+ str(item_num) +')">View full post</button>')
                    h.write('<div id="'+ str(item_num) +'" class="mdwrapper">')
                    if(submission.selftext_html != None):
                        h.write(submission.selftext_html)
                    else:
                        h.write('<p>NO BODY FOR THE SUBMISSION</p>')
                    h.write('</div>\n</div>\n')

            elif isinstance(submission, Comment):
                print('Comment', item_num)
                sub = str(submission.subreddit)
                file_name = sub + '.html'
                with open(file_name, 'a', encoding="utf-8") as h:
                    if sub in subs:
                        print('sub exists, appending')
                    else:
                        #sub files append
                        partialhead(file_name, sub, '../assets/css/style.css')
                        h.write(Head_tag(Span_tag(submission.subreddit_name_prefixed,'s'),1) + "\n")
                        subs.append(sub)
                    h.write('<div class="post">' + '\n')
                    h.write(Head_tag(submission.link_title,2) + '\n')
                    h.write(Span_tag('posted by: u/' + str(submission.author) ,'u'))
                    h.write(Span_tag(str(submission.num_comments) + ' comments', 'c'))
                    h.write(Anchor_tag(submission.permalink, '(source)') + '\n')
                    h.write('<button onclick="toggles('+ str(item_num) +')">View full post</button>')
                    h.write('<div id="'+ str(item_num) +'" class="mdwrapper">')
                    if(submission.body_html!= None):
                        h.write(submission.body_html)
                    else:
                        h.write('<p>NO BODY FOR THE SUBMISSION</p>')
                    h.write('</div>\n</div>\n')

    #sorting all sub reddits alphabetically
    ssub = sorted(subs,key=str.lower)

    #landing page footer content and subs files foter
    partialfooter('Landing.html', ssub)

    #moving landing page to parent folder
    shutil.move('Landing.html', parent_path)
    os.chdir(parent_path)

    #copying assets to output
    sauce = file_path.parent / 'assets'
    destination = parent_path / 'assets'
    shutil.copytree(sauce, destination)
