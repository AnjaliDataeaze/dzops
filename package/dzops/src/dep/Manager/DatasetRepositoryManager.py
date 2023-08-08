import os.path
from dvc.repo import Repo
import git
import os


class DatasetRepositoryManager:
    def init(self):

        git.Repo.init(os.getcwd())
        Repo.init(
            ".",
            force=True,
        )

    def get_url(self, target):
        git.Repo.init(os.getcwd())
        
        s = Repo(os.getcwd())
        s.get_url(target)


    def add(self, target):
        s = Repo(os.getcwd())
        g = git.Repo(os.getcwd())
        print(g)
        s.add(
            targets=target,
            recursive=False,
            no_commit=False,
            fname=None,
            to_remote=False,
        )
    
    def checkout(self, commitid):
        g = git.Repo(os.getcwd())
        g.git.checkout(commitid)

    def list_commits(self):
        g = git.Git(os.getcwd())
        print(g.log('--reflog'))

    def destroy(self):
        s = Repo(os.getcwd())
        s.destroy()

    def commit(self, message):
        g = git.Repo(os.getcwd())
        g.git.add('--all')
        g.git.commit('-m',message)
        print(g)
    
    def clone(self,args):
        git.Git(os.getcwd()).clone(args)

    def remote(self,name:str, data: str, gita: str):
        s = Repo(os.getcwd())
        g = git.Repo(os.getcwd())
        with s.config.edit() as conf:
            conf["core"] = {"remote":"data"}
            conf["remote"]["data"] = {"url": str(data)+'/'+name}
        z=g.create_remote('origin', str(gita))
        print(z)
        g.git.add('--all')
        print(g)

    def push(self):
        s = Repo(os.getcwd())
        g = git.Repo(os.getcwd())
        s.push(remote='data')
        g.git.push("--set-upstream","origin","master")

    def pull(self,file):
        print(os.getcwd())
        s = Repo(os.getcwd())
        s.pull(remote="data",targets=file)
        
    def pull_dataset(self, args):
        print("here")
        s = Repo(os.getcwd())
        s.fetch()
        s.checkout()
        s.pull(remote="remote_store")

    def remote_dataset(self, name: str, args1: str, args2: str):
        s = Repo(os.getcwd())
        g = git.Repo(os.getcwd())

        with s.config.edit() as conf:
            conf["core"] = {"remote": "remote_store"}
            conf["remote"]["remote_store"] = {"url": str(args1) + name}
        if list(g.remotes) is None:
            g.create_remote('origin', str(args2))
