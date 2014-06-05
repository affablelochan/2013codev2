# echo "cleanup GoodRunsLists GoodRunsLists-00-01-03 in /afs/cern.ch/user/t/tamsett/analysis/skims/DataQuality"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /cvmfs/atlas.cern.ch/repo/sw/software/i686-slc5-gcc43-opt/17.2.4/CMT/v1r24
endif
source ${CMTROOT}/mgr/setup.csh
set cmtGoodRunsListstempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if $status != 0 then
  set cmtGoodRunsListstempfile=/tmp/cmt.$$
endif
${CMTROOT}/mgr/cmt cleanup -csh -pack=GoodRunsLists -version=GoodRunsLists-00-01-03 -path=/afs/cern.ch/user/t/tamsett/analysis/skims/DataQuality  -quiet -without_version_directory $* >${cmtGoodRunsListstempfile}
if ( $status != 0 ) then
  echo "${CMTROOT}/mgr/cmt cleanup -csh -pack=GoodRunsLists -version=GoodRunsLists-00-01-03 -path=/afs/cern.ch/user/t/tamsett/analysis/skims/DataQuality  -quiet -without_version_directory $* >${cmtGoodRunsListstempfile}"
  set cmtcleanupstatus=2
  /bin/rm -f ${cmtGoodRunsListstempfile}
  unset cmtGoodRunsListstempfile
  exit $cmtcleanupstatus
endif
set cmtcleanupstatus=0
source ${cmtGoodRunsListstempfile}
if ( $status != 0 ) then
  set cmtcleanupstatus=2
endif
/bin/rm -f ${cmtGoodRunsListstempfile}
unset cmtGoodRunsListstempfile
exit $cmtcleanupstatus

