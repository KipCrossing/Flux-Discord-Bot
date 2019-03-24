import os



class IssueBasedDD(object):

    def __init__(self,issue):
        self.issue = issue
        self.dir_name = self.issue.replace(" ", "_")
        os.mkdir(self.dir_name)



        f = open(self.dir_name + '/records.csv' ,"w+")
        f.write("user\n")
        f.close()

        f_y = open(self.dir_name + '/yes.csv' ,"w+")
        f_y.write("0\n")
        f_y.close()

        f_n = open(self.dir_name + '/no.csv' ,"w+")
        f_n.write("0\n")
        f_n.close()

        pc_y = open(self.dir_name + '/pc_yes.csv' ,"w+")
        pc_y.write("0\n")
        pc_y.close()

        pc_n = open(self.dir_name + '/pc_no.csv' ,"w+")
        pc_n.write("0\n")
        pc_n.close()


    def vote(self,user):
        f = open(self.dir_name + '/records.csv' ,"a")
        check = False
        for line in f:
            user_check = line
            if user_check == user:
                check = True
        if check == False:
            f.close()
            f = open(self.file_name ,"a")
            f.write(str(user) + '\n')
            f.close()



    def vote_yes(self,user):
        self.vote(user)


    def vote_no(self,user):
        self.vote(user)


    def trade(self,user):
        self.vote(user)


    def use_pc(self,user,amount):
        f = open('users/' + user + '.dat','r+')
        bal = int(f[0])
        bal -= amount
        f.write(bal)
        f.close

    def new_user(self,user):
        f = open('users/' + user + '.dat','w+')
        f.write('1.0')
        f.close()

    def user_balance(self,user):
        f = open('users/' + user + '.dat','r+')
        bal = int(f[0])
        return(bal)

    def end(self):
        f = open(self.file_name,'r')
        for line in f:
            vote_info_list = line.split(',')
