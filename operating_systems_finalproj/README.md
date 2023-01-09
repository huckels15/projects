# Project Phase 6: Filesystems
*Team effort (80 pts)*

⚠️ Stanford's Measure of Software Similarity (MOSS) system will be used on this assignment, per [EECS Policy Letter #10](https://github.com/eecs-cs481/course/blob/main/syllabus/10%20Software%20Tools%20to%20Detect%20Similarities.pdf) and the [addendum](https://github.com/eecs-cs481/course/blob/main/syllabus/10%20Enclosure%201%2020220802.pdf) of approved tools. My intent in using this tool is as a deterrent.

*10 bonus points if you turn it in NLT 0730 on 1 Dec (with no grace/late days permitted for the extra credit)*

---

During this phase, you will move away from working in Pintos and instead work directly in a Linux environment. You will modify a skeleton file system implementation that we provide to add support for an in-memory filesystems, called GrayFS. GrayFS is written in C and uses the Filesystem in USErspace (FUSE) library. GrayFS keeps the contents of its files and directories in memory. When the file system is unmounted, the files are gone. Once your work is complete, users will be able to mount your file system into the Linux directory tree and use standard Unix utilities, such as `mkdir`, `cd`, `cat`, `echo`, and `ls` to view the files contained therein.



## Assumptions

* You have completed [Project Phase 5: Performance Analysis](https://github.com/eecs-cs481/course/blob/main/assignments/project/phase5.md)
* You have selected your teammate and sent email to your instructor cc'ing your teammate and documenting your team name.
> 🛑 **DO NOT** enter a team name in Github Classroom until you have received approval from your instructor.
* You have accepted the `phase6` assignment (via the link your instructor sends you when your team and team name get approved) in GitHub Classroom and entered your new team name.

## Artifacts

You must submit the following artifacts no later than the specified times below:

* Source code, electronically submitted using Git - **NLT 0730 on due date**.
* Project write up
    * Individual effort
    * Submit either in your GitHub repo (file = `lastname.md`) or in the box outside your instructor's office (TH1123)
    * Due NLT 0730 on Phase 6 due date (if in GitHub) or the start of your section on Phase 6 due date (if submitted in person).
* [Team feedback](https://forms.office.com/r/bWq1kfM3bM) due NLT 0730 on Phase 6 due date.
* e-Acknowledgement Statement submitted NLT 0730 on due date via CIS.

## Background

UNIX presents a single filesystem tree to its users. Branches within this tree might actually exist in a number of places, such as disks or network locations, but UNIX abstracts this away. The administrative act of grafting a device's filesystem onto the UNIX filesystem tree is called _mounting_.

You can observe what devices make up a particular UNIX computer's filesystem by running the following command:

```
mount
```

Of particular interest in this command's output are columns one and three. Column one indicates the device mounted; for example, `/dev/sda1`, the first partition (`1`) on the first (`a`) internal spinning disk (`sd`). Column three indicates where the device is mounted; for example, `/boot`. The logical location in the filesystem at which a device is mounted is called a _mount point_.  All filesystems begin in a root directory (`/`).

Introducing a new filesystem is a matter of running: `mount <device> <mount point>`. GrayFS takes care of mounting your file system at the mount point that you specify on the command line. Not all directories in Linux can support mounting a file system. We have given you a special place in which to create your mount point: /data/CS481/<first.last>. You should make a new directory called `gfs` (or whatever you like) within your mount directory.
> ⚠️ N.B. The mount point directory (e.g., `gfs`) MUST be empty.

Removing a device from the filesystem when using FUSE is typically a matter of running: `fusermount -u <mount point>`.
> ⚠️ N.B. With this assignment, **you** are responsible for unmounting the file system when you are done testing or using it, even though you don't explicitly mount it. If you run into problem unmounting, you can create a new mount point (e.g., `gfs2`) and keep working; this should (hopefully!) be rare. Any mess that is left behind will be cleaned up at the next reboot.

### User-Level File Systems

The code that implements a filesystem has historically existed in the UNIX kernel, but Linux and other variants of UNIX have support for filesystems that are implemented in user space. When a file system is in user space, the UNIX kernel makes calls to a user-space program that in turn interprets a filesystem for the kernel, almost like a "reverse system call". There are advantages (e.g., ease of implementation, protection against buggy new file systems) and disadvantages (e.g., security, performance) of this approach. Over time, as file systems mature, they are often moved back into the kernel for better performance.

### FUSE

FUSE is one example of a system for supporting user-level file systems. You can learn more about FUSE in its GitHub [repository](https://github.com/libfuse/libfuse) and you will find a couple of examples of FUSE file systems under `examples` in that same repository.

We have provided you with a skeleton FUSE module, called `grayfs.c`, which you should find in your `phase6` repo. We have also provided you a place to create your mount point, called `/data/CS481/<first.last>` where you need to substitute your first and last name. Within this directory, you can create a mount point using `mkdir <mount-point>` where `<mountpoint>` might be "gfs". From a shell, enter your coding directory (i.e., the directory into which you cloned the Phase 6 repository) and run:

```
cd <phase6-coding-directory>
./grayfs -s -f /data/CS481/<first.last>/<mount-point>
```

You can now cd into /data/CS481/<first.last>/<mount-point> and use it like any other directory.

The `grayfs` command above mounts an in-memory filesystem at your mount point with the following options:

* Your file system will run in single-threaded mode ('-s'), which avoids many race conditions and other complications!
* Your file system remains in the foreground ('-f'), which will enable your printf statements to appear.
* You can also enable FUSE debugging output ('-d').

Once you have completed implementation of GrayFS, you should be able to run commands, such as the following:

```
cd /data/CS481/<first.last>/<mount-point>
ls
echo "some content" > /data/CS481/<first.last>/<mount-point>/file
cat /data/CS481/<first.last>/<mount-point>/file
ls -la /data/CS481/<first.last>/<mount-point>
strace ls /data/CS481/<first.last>/<mount-point>      # This might help you debug!
```

### Introduction to GrayFS

We have provided some helper functions to support your in-memory file system. Look at the definitions in `gfs-helper.h`. You can find:

`struct gray_fobj`: This structure manages file system objects, like files, directories, and links. It supports helper functions, such as
* inserting and removing file objects from the directory structure,
* stat'ing file objects,
* reading, writing, and truncating files,
* updating times associated with file objects.

You can look at `gfs-helper.c` to see how these functions are implement.

The skeleton user-level file system is provided in `grayfs.c`. This is the file that you will extend to complete the implementation of GrayFS.

The `struct fuse_operations` structure toward the bottom of the file tells FUSE which functions to call when a particular file system operation is required. It is very similar to the system call table in the Pintos syscall_handler. You will find functions, such as `grayfs_getattr`, `grayfs_mkdir`, `grayfs_rmdir`, `grayfs_readdir`, `grayfs_create`, and the like. Some of these functions first find the required file system object in the file system hierarchy and then call the corresponding helper function to carry out the command. For example, the `grayfs_read` function calls the `gray_read` helper function. Initially, the implementations of the grayfs functions simply print a message to indicate that they were called and then return `-ENOTSUP`. As you implement the functions, more and more file system functionality comes to life!

`main()`: The main function handles any command-line arguments and initializes the file system.

All of this should look rather like your Phase 1 system calls; indeed, the whole concept is like a system call in reverse (i.e., kernel calls user space).

## Instructions

### In-Memory File Objects

We represent file objects in memory using class `FileObj`. This object includes the following fields:

* `type`, which can be type directory, file, link, dev
* `name`, which is the name of this object that is used in pathnames
* `dev`, which tracks the major device number
* `mode`, which controls the access rights for the owner, the group, and everyone else
* `user_id`, which identifies the owner
* `group_id`, which identifies the group
* `access_time`, which tracks the last access time
* `modified_time`, which tracks the last time the file was modified
* `status_change_time`, which tracks the last time the status was modified
* `extended_attr`, which tracks a dictionary of attributes
* `content`, which tracks the content of this file object (see details below)

An object's `content` field differs based on the type of the object.
* For a regular file, the content is a **string** that represents the contents of the file.
* For a symbolic link, the content is a **string** representing the pathname to the base object.
* For a directory, the content is a **set** that holds the children's file objects.

### Useful GrayFS Functions

You will need to make use of the following GrayFS functions during the course of completing this project:

1. The `gfs-helper.c` file provides some helper functions that you may find useful:

    ```C
    // Gets the directory component of a pathname (strips the final component)
    // Destructive to the path sent in
    char *gray_dirname(char *path);

    // Gets the final component of the pathname (often the file name)
    // Destructive to the path sent in
    char *gray_basename(char *path);

    // Initializes a file object obj, setting its type and component name
    void init_fobj(struct gray_fobj* obj, enum FileType type, char *name);

    // Get the FileObj referenced by path starting at the root
    struct gray_fobj *getFileObject(struct gray_fobj *root, char *path);

    // Given a path and a starting file object, crawl the path to find
    // the file object associated with the final component of the path
    struct gray_fobj *gray_child(struct gray_fobj *start, char *path) {

    // Insert a child object into the parent object
    void gray_insert(struct gray_fobj *parent, struct gray_fobj *child);

    // Remove a child object from its parent
    void gray_remove(struct gray_fobj *object);

    // Returns an struct stat object based on the attributes of the given
    // file object
    void gray_stat(struct gray_fobj *object, struct stat *stat_buf);

    // Read length bytes starting at offset in the specified file
    char *gray_read(struct gray_fobj *file, int offset, int length);

    // Write buffer to the specified file, starting at offset
    int gray_write(struct gray_fobj *file, int offset, char *buffer);

    // Truncate the specified file to the specified length
    void gray_truncate(struct gray_fobj *file, int length);

    // Updates the time of last access, modification, and/or status change
    // of the object to the current time
    void updateTimes(struct gray_fobj *object, bool accessed, bool modified,
                     bool status);
    ```

1. FUSE provides a filler function to help you implement `readdir`.

    ```C
    // FUSE provides a filler function to help you create directory entries
    // in your buffer. It wants five arguments. For the final three parameters,
    // send it: NULL, 0, and 0.
    int filler(void *buf, char *filename, struct stat *st, int offset, int unknown)
    ```


### Programming

1. You will need to implement the file system functions for the following basic calls:

    ```C
    // Get the file's attributes
    static int grayfs_getattr(const char *path, struct stat *stbuf,
                              struct fuse_file_info *fi)
    ```
2. You will need to implement the following directory-related calls:

    ```C
    // Create the directory of the give name with the specified mode
    int grayfs_mkdir(const char *path, mode_t mode)

    // Remove the directory of the given name
    int grayfs_rmdir(const char *path)

    // Return one or more directory entries
    static int grayfs_readdir(const char *path, void *buf,
                              fuse_fill_dir_t filler,
                              off_t offset, struct fuse_file_info *fi,
                              enum fuse_readdir_flags flags)
    ```
3. You will need to implement the following file-related calls:

    ```C
    // Create a file object named path with the given flags and mode
    int grayfs_create(const char *path, mode_t mode, struct fuse_file_info *fi)

    // Truncate the file specified by path to the given length
    static int grayfs_truncate(const char *path, off_t size,
                               struct fuse_file_info *fi)

    // Open the file object specified by path
    static int grayfs_open(const char *path, struct fuse_file_info *fi)

    // Read length bytes from the file specified by path starting at offset
    static int grayfs_read(const char *path, char *buf, size_t size, off_t offset,
                           struct fuse_file_info *fi)

    // Write the buffer into the file specified by path starting at offset
    static int grayfs_write(const char *path, const char *buf, size_t size,
                            off_t offset, struct fuse_file_info *fi)

    // Delete the specified file, link, or special file
    static int grayfs_unlink(const char *path)

    // Rename the file object from oldpath to newpath
    static int grayfs_rename(const char *from, const char *to, unsigned int flags)
    ```

4. You will need to implement the following functions related to special files and links:

    ```C
    // Create a special file, such as a device, FIFO, or socket
    static int grayfs_mknod(const char *path, mode_t mode, dev_t rdev)

    // Create a symbolic link from newpath to path
    static int grayfs_symlink(const char *from, const char *to)

    // Return the target of the link
    static int grayfs_readlink(const char *path, char *buf, size_t size)
    ```

5. You will need to implement the following functions related to access control:

    ```C
    // Change the mode of the file object
    static int grayfs_chmod(const char *path, mode_t mode,
                            struct fuse_file_info *fi)

    // Change the owner and/or group of the file object
    static int grayfs_chown(const char *path, uid_t uid, gid_t gid,
                            struct fuse_file_info *fi)

    // Change the last access and modified times of the file object where:
    //     times[0] is the last access time
    //     times[1] is the last modified time
    int grayfs_utimens(const char *path, const struct timespec tv[2],
                       struct fuse_file_info *fi)
    ```


Using `grayfs.c` as a starting point, complete the implementation of the **FUSE** module that implements the in-memory file system.

### Where to start

As in your Phase 1 assignment, you want to consider the order in which you implement the various file system calls needed to complete the assignment. Because you are now experienced system programmers, we will leave the order of implementation to you with two hints and one reminder:

### Hints:
1. `getattr` is called approximately 2 bajillion times (yes, I counted)
2. `strace` is your friend

⚠️ Reminder: Implement the smallest number of calls and test those before continuing on to the next call(s).

### Testing

Your completed implementation should support the standard Unix commands, such as those shown below, with the corresponding output. Assume <rootdir> is /data/CS481/<first.last>/<mount-point>.

_Terminal 1:_

```
cd <phase6-working-directory>
./grayfs <rootdir>
```

_Terminal 2:_

```
eecslinux> cd <rootdir>
eecslinux> echo foo contents > foo.txt
eecslinux> cat foo.txt
foo contents
eecslinux> echo bar contents > bar.txt
eecslinux> cat bar.txt
bar contents
eecslinux> cat foo.txt bar.txt > baz.txt
eecslinux> cat baz.txt
foo contents
bar contents
eecslinux> ls -la foo.txt
-rw------- 2 maria.ebling eecs-linux-faculty 4 Nov 18 06:50 foo.txt
eecslinux> touch foo.txt
eecslinux> ls -la foo.txt
-rw------- 2 maria.ebling eecs-linux-faculty 4 Nov 18 06:52 foo.txt
eecslinux> ls -la bar.txt
-rw------- 2 maria.ebling eecs-linux-faculty 4 Nov 18 06:50 bar.txt
eecslinux> chmod 666 bar.txt
eecslinux> ls -la bar.txt
-rw-rw-rw- 2 maria.ebling eecs-linux-faculty 4 Nov 18 06:50 bar.txt
eecslinux> ln -s foo.txt foosymlink
eecslinux> mkdir folder
eecslinux> ls -la
total 6
drwxr-xr-x 2 maria.ebling eecs-linux-faculty    3 Nov 18 07:43 .
drwx------ 4 maria.ebling eecs-linux-faculty 4096 Nov 18 10:20 ..
drwx------ 2 maria.ebling eecs-linux-faculty    2 Nov 18 07:43 folder
-rw------- 2 maria.ebling eecs-linux-faculty    4 Nov 18 07:43 foo.txt
lrw-r--r-- 2 maria.ebling eecs-linux-faculty    3 Nov 18 10:33 foosymlink -> foo.txt
eecslinux> cat foosymlink
foo contents
eecslinux> rm foo.txt
rm: remove regular file ‘foo.txt’? y
eecslinux> ls -la
total 6
drwxr-xr-x 2 maria.ebling eecs-linux-faculty    2 Nov 18 07:43 .
drwx------ 4 maria.ebling eecs-linux-faculty 4096 Nov 18 10:20 ..
drwx------ 2 maria.ebling eecs-linux-faculty    2 Nov 18 07:43 folder
lrw-r--r-- 2 maria.ebling eecs-linux-faculty    3 Nov 18 10:33 foosymlink -> foo.txt
eecslinux> cat foosymlink
cat: foosymlink: No such file or directory
eecslinux> rmdir folder
```

Other commands (not shown here) may also be used to test your file system.

Refer to the comments above each file system call in `grayfs.c` and `gfs-helper.c` as well as to the referenced manual pages if you have a question about what a system call is supposed to do. As noted earlier, running commands with `strace` can help you figure out what system calls were made.

### Error Handling

As with other phases of the CS481 projects, you will need to handle errors.

The error codes most useful for Phase 6 include:

* `EEXIST` -- File exists. Typically, this error results when something is expected NOT to exist, but does, in fact, exist. For example, if the target of `mkdir` or `mknod` already exists, this would be the error returned by the file system.

* `EISDIR` -- Is a directory. Typically, this error results when a pathname was not expected to be a directory, but is, in fact, a directory. For example, your file system should return this error in the event that the user attempts to read a directory, such as by calling `cat <rootdir>/folder` where the `folder` component is a directory rather that a regular file.

* `ENOTDIR` -- Not a directory. Typically, this error results when some pathname was expected to be a directory, but is, in fact, NOT a directory. For example, your file system should return this error if the user tries to access `<rootdir>/component1/component2`, but `component1` is a file rather than a directory.

* `ENOENT` -- No such file or directory. Typically, this error results from trying to perform a function on a pathname that doesn't exist, either because one of the components of the pathname doesn't exist or because the final entry of the pathname doesn't exist. It can also result when following a "dangling" symbolic link, such as when the source of the symlink has been removed, but the symlink still remains

* `ENOTSUP` -- Function not supported. Typically, this error results when a file system function has not (yet) been implemented. The skeleton code we have given you returns `-ENOTSUP` for all the functions that you need to implement. You will need to remove this return value once your implementation is complete.

* `ENOTEMPTY` -- Directory not empty. Typically, this error results when a directory was expected to be empty, but wasn't. For example, `rmdir` expects to operate on an empty directory.

Other error numbers and their description can be found in the `errno(3)` manual page.

### Write up
Answer the following questions individually, placing your answers in a file named 'lastname.md' where 'lastname' is your last name:

1. Do you want to be a kernel developer, why or why not? Put some serious thought into this and your justification.

1. How much time did you spend on this project?

1. Order the phases of the project by difficulty level and effort required.

    a. Phase 0 - code review of a system call

    b. Phase 1 - implement file-related system calls

    c. Phase 2 - implement process-related system calls

    d. Phase 3 - implement message passing (i.e., mailboxes)

    e. Phase 4 - implement swapping

    f. Phase 5 - implement nice, instrument kernel, and performance evaluation

    g. Phase 6 - implement a user-level file system

1. Identify the projects that helped you learn the most and the least.

1. What did you find the most/least interesting about the class?

1. What do you wish we would have covered but did not?


## Grading
While the following will guide the grading of this project phase, your instructor reserves the right to deviate from this plan:

| Component  | Points |
| --- | --- |
|Correct implementation of file system calls  |50 |
|Code is well-designed, clean, and descriptive  |15 |
|Write up is complete  |10|
|eACK and team feedback completed on time| 5 |
