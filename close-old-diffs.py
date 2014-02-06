#!/usr/bin/python

from phabricator import Phabricator
import datetime

phab = Phabricator()  # This will use your ~/.arcrc file
phid = phab.user.whoami()['phid']
diffs = phab.differential.query(status="status-open", reviewers=[phid])
now = datetime.datetime.now()
print phid

for diff in diffs:
  print diff
  if int(diff['status']) == 0:
    print diff['id']
    dateCreated = datetime.datetime.fromtimestamp(int(diff['dateCreated']))
    print dateCreated
    daysOld = divmod((now - dateCreated).total_seconds(), 60*60*24)[0]
    print '%d days old' % daysOld
    if daysOld > 60:
      print 'closing %s, too old' % diff['id']
      phab.differential.createcomment(
        revision_id=int(diff['id']),
        message='auto-closing because it is more than 60 days old',
        action='accept',
        silent=True
      )

