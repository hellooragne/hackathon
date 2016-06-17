#!/usr/bin/perl -w

# Convergence FreeSWITCH(tm) Tools Version 7.0
# (c) MMII Convergence. All rights reserved.
# <info@convergence.pk> http://www.convergence.pk

# This program is free software, distributed under the terms of
# the GNU General Public License.http://www.gnu.org/licenses.html

use strict;
use DBI();
use File::Copy;

# this command sends -SIGHUP to fs, she creates new cdr.csv files, so we can load the old ones up
my @cc  = ("killall", "-HUP", "freeswitch");
system(@cc) == 0 or die "$0: system @cc failed: $?";

#my $dbh = DBI->connect("DBI:mysql:database=freeswitch;host=10.253.31.4","root","123456") or die "$0: Couldn't connect to database: " . DBI->errstr;
my $dbh = DBI->connect("dbi:mysql:freeswitch:mysql_local_infile=1:127.0.0.1:3306","root","hackathon") or die "$0: Couldn't connect to database: " . DBI->errstr;

# this is the standard location of the cdr-csv
my @LS  = `ls -1t /home/hackathon/log/cdr-csv/Master.csv.*`;
foreach my $line (@LS) {
    chop($line);
    my $stm     = "LOAD DATA LOW_PRIORITY LOCAL INFILE '$line' INTO TABLE cdr FIELDS ENCLOSED BY '\"' TERMINATED BY ','";
    my $ul      = $dbh->prepare($stm) or die "$0: Couldn't prepare statement $stm: " . $dbh->errstr;;
    $ul->execute();
    $ul->finish;
    system("cat $line >> /home/hackathon/log/cdr-csv/FULL_Master.csv"); # we do this to maintain a single FULL file if needed
    unlink $line;
}

# one silly thing is that each accountcode has its own cdr.csv as well, either handle those here, by loading them into their own tables, or rm them
my @BS  = ("xtec","megaphone","mafcom","xeivacom");
foreach my $code (@BS) {
   @LS = `ls -1t /usr/local/freeswitch/log/cdr-csv/$code.csv.*`;
   foreach my $line (@LS) {
       chop($line);
       #unlink($line);  #to delete
       move($line, "/usr/local/freeswitch/log/cdr-csv/trash/$code/"); # or move into a separate dir for later procession
   }
}

exit 0;
