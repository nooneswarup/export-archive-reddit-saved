import praw, os, config, pickle, shutil
from praw.models import Submission

#importing configs and PRAW
reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent,
                     username=config.username,
                     password=config.password)
#testing these functions
def runn(post):
    if isinstance(post, Submission):
            print('Post', post.id)
            sub = str(post.subreddit)
            file_name = sub + '.html'
            partialhead(file_name, sub, '../assets/css/style.css')
            h=open(file_name, 'a', encoding="utf-8")
            h.write(Rh(Rs(post.subreddit_name_prefixed,'s'),1) + "\n")
            # subs.append(sub)
            post = newsyncpost(post)
            h.write(post)
            h.close()

def newsyncpost(post):
    print('Inside newsyncpost function')
    title = Rh(post.title,2)
    author = Rs('posted by: u/' + str(post.author) ,'u')
    num_comments = Rs(str(post.num_comments) + ' comments', 'c')
    post_url = Ra(post.url, '(source)')
    item_num = str(post.id)

    if(post.selftext_html != None):
        value = post.selftext_html
    else:
        value = '<p>NO BODY FOR THE POST</p>'

    new_post = """<div class="post">
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

    write_post = new_post.format(title, author, num_comments, post_url, item_num, item_num, value)
    print(write_post)
    return write_post

def rerun(post):
    #check if sub file exists
    new_sub_list = []
    print('Inside rerun function')
    print(post)
    print(os.getcwd())
    print(post.subreddit)
    sub = str(post.subreddit) + ".html"
    if (os.path.isfile(sub)):
        #if file exists then append new post
        f = open(sub, 'r', encoding="utf-8")
        contents = f.readlines()
        f.close()
        #add new_post function
        new_post = newsyncpost(post)
        print('return post html')
        contents.insert(12, new_post)

        f = open(sub, 'w', encoding="utf-8")
        contents = "".join(contents)
        f.write(contents)
        f.close()
    else:
        print('New sub detected, creating new file')
        runn(post)
        new_sub_list.append(str(post.subreddit))
        print(new_sub_list)
    return new_sub_list

#functions
def Rh(data,num):
    num = str(num)
    data = str(data)
    data = '<h'+ num +'>'+ data + '</h'+num+'>'
    return data

def Rp(data):
    data = str(data)
    data = '<p>'+ data +'</p>'
    return data

def Rs(data,c):
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

def Ra(data, source):
    data = str(data)
    data = '<a href="' + data + '" target="_blank">'+ source + '</a>'
    return data

def partialhead(file_name,title, ref_path):
    file_name = str(file_name)
    f = open(file_name, 'a', encoding="utf-8")
    l1 = '<!DOCTYPE html>'
    l2 = '<html>'
    l3 = '<head>'
    l4 = '    <meta charset="utf-8">'
    l5 = '    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
    l6 = '    <title>'+ str(title) +'</title>'
    l7 = '    <link href="https://fonts.googleapis.com/css?family=Sniglet|Open+Sans:400,700&display=swap" rel="stylesheet">'
    l8 = '    <link rel="stylesheet" href="' + ref_path + '">'
    l9 = '</head>'
    l10 = '<body>'
    l11= '    <div class="container">'
    lines = [l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11]
    f.writelines("%s\n" % l for l in lines)
    f.close()

def partialfooter(file_name, ssub):
    file_name = str(file_name)
    f = open(file_name, 'a', encoding="utf-8")
    l1 = '    <div class="dropdown">'
    l2 = '        <input type="text" id="myInput" onkeyup="filterlist()" placeholder="Search here.." title="Search for subs">'
    l3 = '        <button class= "dropbtn">Subreddits</button>'
    l4 = '        <div class="dropdown-content">'
    l5 = '        <ul class="landinglist" id ="filterlist">'
    lines = [l1,l2,l3,l4,l5]
    f.writelines("%s\n" % l for l in lines)
    for a in ssub:
        print(a)
        h = open(a+ '.html', 'a', encoding="utf-8")
        h.write('</div>' + '\n')
        h.write('<script src="../assets/js/script.js"></script>' + "\n")
        h.write('</body></html>')
        h.close()
        l6 = '<li>' + Ra("subs/"+ a + ".html", 'r/' + a)+ '</li>' + "\n"
        f.write(l6)
    l7 = '        </ul>'
    l8 = '</div></div></div>'
    l9 = '<script src="assets/js/script.js"></script>'
    l10 = '</body></html>'
    lines = [l7,l8,l9,l10]
    f.writelines("%s\n" % l for l in lines)
    f.close()

def syncload():
    with open('sync.p', 'rb') as h:
        recent_id = str(pickle.load(h))
        print('Now loading recently saved id:')
        print(recent_id)
        return recent_id
        h.close()

def syncdump(postid):
    with open('sync.p','wb') as f:
        print('updating most recent id:')
        print(postid)
        pickle.dump(postid, f)
        f.close()

def newrecent():
    saved = reddit.user.me().saved(limit=1)
    for post in saved:
        print('recent id:')
        print(post.id)
        postid = str(post.id)
        return postid

print(reddit.read_only)
#get current working directory
print(os.getcwd())
file_path =  os.getcwd()
#get login user name
loginuser = str(os.getlogin())
print(loginuser)
#changing path
paths = 'C:\\Users\\'+ loginuser +'\\Desktop'
os.chdir(paths)
print(os.getcwd())
print('changing directory to desktop and creating new folder')
directory = '\\Redditsaved'
new_path = paths + directory + '\\subs'
if not os.path.exists(directory):
    if not os.path.exists(new_path):
        print('making new path')
        os.makedirs(new_path)
os.chdir(new_path)
print(os.getcwd())


#check if file exits #if exists
if (os.path.isfile('sync.p')):
    #if true get id
    print('Syncing')
    recent_id = syncload()
    #compare with new id
    saved = reddit.user.me().saved(limit=1000)
    for post in saved:
        postid = str(post.id)
        print('Processing post with id:')
        print(postid)
        if(recent_id == postid):
            #if compare is true break
            print('No new posts: terminating sync')
            break;
        else:
            print('Syncing this id')
            new_subs = rerun(post)
            print('worked')
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

#if file does not exists #proram runs for first time and creates the file
else:
    postid = newrecent()
    syncdump(postid)
    # generating a listing generator PRAW to get all savd items
    saved = reddit.user.me().saved(limit=1000)
    # counter for total number of saved items
    item_num = 0
    #all sub reddits list
    subs = []
    allpostids =[]

    #landing page header and h1
    f = open('Landing.html', 'a', encoding="utf-8")
    partialhead('Landing.html', 'Reddit is saved', 'assets/css/style.css')
    f.write('<h1 class="title">"Reddit is saved"</h1>')
    f.close()

    #looping through all saved items
    for post in saved:
            item_num += 1
            allpostids.append(str(post.id))
            if isinstance(post, Submission):
                print('Post', item_num)
                sub = str(post.subreddit)
                file_name = sub + '.html'
                h=open(file_name, 'a', encoding="utf-8")
                if sub in subs:
                    print('sub exists, appending')
                else:
                    #sub files append
                    partialhead(file_name, sub, '../assets/css/style.css')
                    h.write(Rh(Rs(post.subreddit_name_prefixed,'s'),1) + "\n")
                    subs.append(sub)
                h.write('<div class="post">' + '\n')
                h.write(Rh(post.title,2) + '\n')
                h.write(Rs('posted by: u/' + str(post.author) ,'u'))
                h.write(Rs(str(post.num_comments) + ' comments', 'c'))
                h.write(Ra(post.url, '(source)') + '\n')
                h.write('<button onclick="toggles('+ str(item_num) +')">View full post</button>')
                h.write('<div id="'+ str(item_num) +'" class="mdwrapper">')
                if(post.selftext_html != None):
                    h.write(post.selftext_html)
                else:
                    h.write('<p>NO BODY FOR THE POST</p>')
                h.write('</div>')
                h.write('\n</div>\n')
                h.close()

            else:
                print('comment will do something later')
                print('Comment', item_num)
                #see comment only, moved for clutter=>need to edit later

    #sorting all sub reddits alphabetically
    ssub = sorted(subs,key=str.lower)

    #landing page footer content and subs files foter
    partialfooter('Landing.html', ssub)

    #moving landing file to parent folder
    landingpath = os.getcwd()
    print(landingpath)
    landingpath += '\\Landing.html'
    shutil.move('Landing.html' , paths + directory)
    os.chdir("../..")

    sauce = file_path
    sauce += "\\assets"
    destination = paths + directory + '\\assets'
    print(destination)
    shutil.copytree(sauce, destination)
