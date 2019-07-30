#!/usr/bin/env python
#coding=utf-8

from urllib import request
import datetime
import shutil
import json

def get_html():
    html_text = request.urlopen("http://contests.sdutacm.cn/contests.json").read()
    return json.loads(html_text)

def change_time(time_str):
    time_crude = time_str.split('T')[0]
    time_out = time_crude + '  ' +time_str.split('T')[1].strip('Z')
    time_ripe = time_crude.split('-')
    time_competition = datetime.date(int(time_ripe[0]), int(time_ripe[1]), int(time_ripe[2]))
    time_today = datetime.date.today()
    return (time_competition - time_today).days,time_out

def create_html(html_json):

    shutil.copyfile('model.html','recentcontests.html')
    tr_model = '<tr class="%s"><td>%s</td><td><a href="%s" target="_blank" >%s</a></td><td>%s</td><td>%s</td></tr>\n'
    tab = ""

    f = open('recentcontests.html','a',encoding='utf-8')
    for index in range(len(html_json)-1):
        i = html_json[index]
        time_interval,time_out = change_time(i["start_time"])
        if time_interval < 0:
            continue
        if time_interval == 0 or time_interval ==1:
            tab=tr_model%('odd' if index%2==0 else '', i["source"], i["link"], i["name"],time_out, str(time_interval)+'days' if time_interval>1 else str(time_interval)+'day')
        else:
            tab=tr_model%('odd' if index%2==0 else '', i["source"], i["link"], i["name"], time_out, str(time_interval)+'days' if time_interval>1 else str(time_interval)+'day')
        f.write(tab)
    final = '\n</table><center><p>Copyright &copy; 2012. All right reserved. Design by <a href="https://github.com/ma6174/recentcontest">ma6174</a></p></center></body></html>'
    f.write(final)
    f.close()
    print('完成')

if __name__=='__main__':
    html_json = get_html()
    create_html(html_json)
