#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/ptrace.h>
#include <sched.h>
#include <sys/user.h>
#include <sys/syscall.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <errno.h>

struct child_args {
    char *path;
    uid_t uid;
};

struct track_processes {
    pid_t g_pid;
};

int remove_from_table(pid_t pid, struct track_processes *procs){
    for (int i = 0; i < 3; i++){
        if (procs[i].g_pid == pid){
            procs[i].g_pid = -1;
            return 0;
        }
    }
    return -1;
}

int check_exists(pid_t pid, struct track_processes *procs){
    for (int i = 0; i < 3; i++){
        if (procs[i].g_pid == pid){
            return 1;
        }
    }
    return 0;
}

int add_to_table(pid_t pid, struct track_processes *procs){
    for (int i = 0; i < 3; i++){
        if (procs[i].g_pid == -1){
            procs[i].g_pid = pid;
            return 1;
        }
    }
    return 0;
}

int handle_connect(pid_t pid, int sig, int status, struct user_regs_struct regs){
    long peek[2];
    struct sockaddr_in sock;
    int valid = 0;

    for (int i = 0; i < 2; i++){
        peek[i] = ptrace(PTRACE_PEEKDATA, pid, regs.rsi + i *sizeof(long), NULL);
    }
    memcpy(&sock, peek, sizeof(sock));

    char *ip = inet_ntoa(sock.sin_addr);
    char *ip_cpy = malloc(strlen(ip));

    if (ip_cpy == NULL){
        fprintf(stderr, "Malloc failed.");
        return -1;
    }

    strncpy(ip_cpy, ip, 16);

    char *ip_decomp[4];
    char *tok = strtok(ip, ".");

    for (int i = 0; i < 4; i++){
        ip_decomp[i] = tok;
        tok = strtok(NULL, ".");
    }

    if (strcmp(ip_decomp[0], "127") == 0 && strcmp(ip_decomp[1], "0") == 0 && strcmp(ip_decomp[2], "0") == 0){
        valid = 1;
    }

    if (valid == 0){
        regs.orig_rax = -1;
        ptrace(PTRACE_SETREGS, pid, NULL, &regs);
        ptrace(PTRACE_SYSCALL, pid, NULL, sig);
        waitpid(pid, &status, 0);
        regs.rax = -EPERM;
        ptrace(PTRACE_SETREGS, pid, NULL, &regs);
    }

    free(ip_cpy);
    return 0;

}

int child_exec(void *args){

    struct child_args *arguments = (struct child_args *)args;

    if (chdir(arguments->path) == -1){
        fprintf(stderr, "Chdir failed.");
        return -1;
    }

    if (setuid(arguments->uid) == -1){
        fprintf(stderr, "Setuid failed.");
        return -1;
    }

    ptrace(PTRACE_TRACEME, NULL, NULL, NULL);
    if (execlp("python3", "python3", "guest.pyc", NULL) == -1){
        fprintf(stderr, "Exec failed.");
        return -1;
    }
    return 0;
}

int main(int argc, char *argv[]){

    int status;
    int max_proc = 3;

    if (argc != 3){
        fprintf(stderr, 
        "Usage for %s: \nFirst input: Path to guest dir\nSecond input: UID for privilege to be used for guest.pyc",
        argv[0]);
        return -1;
    }

    struct child_args *args = malloc(sizeof(struct child_args));
    
    if (args == NULL){
        fprintf(stderr, "Malloc failed.");
        return -1;
    }

    void *stack = malloc(1024 * 1024);
    if (stack == NULL){
        fprintf(stderr, "Malloc failed.");
        return -1;
    }

    args->path = argv[1];
    args->uid = atoi(argv[2]);

    struct track_processes processes[max_proc];

    pid_t child_pid = clone(
        child_exec, 
        stack + (1024 * 1024), 
        CLONE_NEWPID,
        args
        );

    if (child_pid == -1){
        fprintf(stderr, "Clone failed.");
        return -1;
    }

    sleep(1);

    processes[0].g_pid = child_pid;
    processes[1].g_pid = -1;
    processes[2].g_pid = -1;

    ptrace(PTRACE_SETOPTIONS, child_pid, NULL, PTRACE_O_TRACECLONE | PTRACE_O_TRACEFORK | PTRACE_O_TRACEVFORK | PTRACE_O_EXITKILL);

    for (;;){
        pid_t forked_pids = wait(&status);
        int sig_to_pass = 0;
        if (forked_pids < 0){
            free(args);
            free(stack);
            return 0;
        }

        if (WIFEXITED(status) || WIFSIGNALED(status)){
            remove_from_table(forked_pids, processes);
        }

        if (WIFSTOPPED(status)){
            sig_to_pass = WSTOPSIG(status);
            if (sig_to_pass == SIGTRAP){
                sig_to_pass = 0;
                struct user_regs_struct regs;
                ptrace(PTRACE_GETREGS, forked_pids, NULL, &regs);

                int exists = check_exists(forked_pids, processes);

                if (exists == 1 && regs.orig_rax == SYS_connect){
                    handle_connect(forked_pids, sig_to_pass, status, regs);
                }
                
                if (exists == 0){
                    int add = add_to_table(forked_pids, processes);

                    if (add == 0){
                        kill(forked_pids, SIGKILL);
                    }
                }
            }
        }

        ptrace(PTRACE_SYSCALL, forked_pids, NULL, sig_to_pass);

    }

    free(args);
    free(stack);

    return 0;
}