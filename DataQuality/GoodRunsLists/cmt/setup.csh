# echo "setup GoodRunsLists GoodRunsLists-00-01-03 in /afs/cern.ch/user/t/tamsett/analysis/skims/DataQuality"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /cvmfs/atlas.cern.ch/repo/sw/software/i686-slc5-gcc43-opt/17.2.4/CMT/v1r24
endif
source ${CMTROOT}/mgr/setup.csh
set cmtGoodRunsListstempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if $status != 0 then
  set cmtGoodRunsListstempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt setup -csh -pack=GoodRunsLists -version=GoodRunsLists-00-01-03 -path=/afs/cern.ch/user/t/tamsett/analysis/skims/DataQuality  -quiet -without_version_directory -no_cleanup $* >${cmtGoodRunsListstempfile}
if ( $status != 0 ) then
  echo "${CMTROOT}/mgr/cmt setup -csh -pack=GoodRunsLists -version=GoodRunsLists-00-01-03 -path=/afs/cern.ch/user/t/tamsett/analysis/skims/DataQuality  -quiet -without_version_directory -no_cleanup $* >${cmtGoodRunsListstempfile}"
  set cmtsetupstatus=2
  /bin/rm -f ${cmtGoodRunsListstempfile}
  unset cmtGoodRunsListstempfile
  exit $cmtsetupstatus
endif
set cmtsetupstatus=0
source ${cmtGoodRunsListstempfile}
if ( $status != 0 ) then
  set cmtsetupstatus=2
endif
/bin/rm -f ${cmtGoodRunsListstempfile}
unset cmtGoodRunsListstempfile
exit $cmtsetupstatus

