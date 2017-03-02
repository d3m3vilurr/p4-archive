# -*- coding: utf-8 -*-
import os
import tarfile
import tempfile
from P4 import P4, DepotFile
import flask
import config as CONFIG

app = flask.Flask(__name__)

p4 = P4()
p4.port = CONFIG.P4_PORT
p4.user = CONFIG.P4_USER
p4.password = CONFIG.P4_PASSWD

p4.connect()
p4.run_login()

def download_archive(depot_rule=CONFIG.DEFAULT_DEPOT_PATH,
                     branch=CONFIG.DEFAULT_BRANCH,
                     repo=CONFIG.DEFAULT_REPO):
    #print depot_rule
    #print branch, repo
    depot = depot_rule % dict(branch=branch, repo=repo)
    prefix = os.path.split(depot)[0]
    out = tempfile.NamedTemporaryFile(delete=False)
    with tarfile.open(mode='w:gz', fileobj=out) as w:
        for file_info in p4.run('files', depot + '/...'):
            #print file_info['depotFile'],
            if 'delete' in file_info['action']:
                #print 'was deleted'
                continue
            data = p4.run('print', '%s#%s' % (file_info['depotFile'], file_info['rev']))
            b = tempfile.NamedTemporaryFile()
            b.write(''.join(data[1:]))
            b.flush()
            w.add(b.name, file_info['depotFile'].lstrip(prefix))
            #print 'done'
    return out.name

@app.route('/archive/<repo>/<branch>.tar.gz')
def download(repo, branch):
    filename = download_archive(branch=branch, repo=repo)

    @flask.after_this_request
    def remote_temp_file(resp):
        os.unlink(filename)
        os.path.exists(filename)
        return resp

    return flask.send_file(filename,
                           attachment_filename=('%s.tar.gz' % branch))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
