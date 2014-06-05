# echo "cleanup GoodRunsLists GoodRunsLists-00-01-03 in /afs/cern.ch/user/t/tamsett/analysis/skims/DataQuality"

if test "${CMTROOT}" = ""; then
  CMTROOT=/cvmfs/atlas.cern.ch/repo/sw/software/i686-slc5-gcc43-opt/17.2.4/CMT/v1r24; export CMTROOT
fi
. ${CMTROOT}/mgr/setup.sh
cmtGoodRunsListstempfile=`${CMTROOT}/mgr/cmt -quiet build temporary_name`
if test ! $? = 0 ; then cmtGoodRunsListstempfile=/tmp/cmt.$$; fi
${CMTROOT}/mgr/cmt cleanup -sh -pack=GoodRunsLists -version=GoodRunsLists-00-01-03 -path=/afs/cern.ch/user/t/tamsett/analysis/skims/DataQuality  -quiet -without_version_directory $* >${cmtGoodRunsListstempfile}
if test $? != 0 ; then
  echo >&2 "${CMTROOT}/mgr/cmt cleanup -sh -pack=GoodRunsLists -version=GoodRunsLists-00-01-03 -path=/afs/cern.ch/user/t/tamsett/analysis/skims/DataQuality  -quiet -without_version_directory $* >${cmtGoodRunsListstempfile}"
  cmtcleanupstatus=2
  /bin/rm -f ${cmtGoodRunsListstempfile}
  unset cmtGoodRunsListstempfile
  return $cmtcleanupstatus
fi
cmtcleanupstatus=0
. ${cmtGoodRunsListstempfile}
if test $? != 0 ; then
  cmtcleanupstatus=2
fi
/bin/rm -f ${cmtGoodRunsListstempfile}
unset cmtGoodRunsListstempfile
return $cmtcleanupstatus

