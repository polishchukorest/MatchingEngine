# MatchingEngine  

!warning: the lightmatchingengine module (from https://github.com/gavincyi/LightMatchingEngine) last version should be installed, pip install will install version   !2019.1.4 that contains errors (https://github.com/gavincyi/LightMatchingEngine/issues/13), in my case I've changed the source code which is loaded to this repository  


1. The solution used one of the open source machine engines that were provided: https://github.com/gavincyi/LightMatchingEngine, the problems with the class that were resolved is described previously. This option (https://jellepelgrims.com/posts/matching_engines) was declined by me, due to the sketchiness. https://github.com/jpelgrims/matching_engine here it's described as prototype.  
2. First of all, the script loads two files, merges them, adds fictional price for the market orders and sorts them by time.  
3. Next, I iterate over all of them, load to the Matching Engine and write to the resulting trades file.  
4. The resulting csv was checked in Jupyter to be more presentable.  
