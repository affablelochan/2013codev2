class TreeReader:
   def __init__(self,tree=None):
       self.TREE=tree
       self.CacheSize=10000000
       self.CacheLearning=True
       self.CacheLearningEvts=10
       if self.CacheLearning and tree != None:
          tree.SetCacheSize(self.CacheSize)
          tree.SetCacheLearnEntries(self.CacheLearningEvts)
       self.CurrentEntry=0
       self.BRANCHES={}
       return

   def SetEntry(self,chainEntry):
       if self.TREE == None:
          return None
       self.CurrentEntry = self.TREE.LoadTree(chainEntry)
       if self.CurrentEntry == 0:
          self.BRANCHES={}
       return self.CurrentEntry

   def ReadBranch(self,brName):
       fBranches = self.BRANCHES
       entry = self.CurrentEntry
       if brName in fBranches:
          [branch,lastEntry,value] = fBranches[brName]
          if lastEntry == entry:
             return value
          else:
             branch.GetEntry(entry,1)
             value = getattr(self.TREE,brName)
             fBranches[brName][1] = entry
             fBranches[brName][2] = value
             return value
       else:
          branch = self.TREE.GetBranch(brName)
          if branch == None:
             return None
          else:
             branch.GetEntry(entry,1)
             value = getattr(self.TREE,brName)
             fBranches[brName] = [branch,entry,value]
             return value
