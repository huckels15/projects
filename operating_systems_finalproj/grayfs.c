/*
 * Long Gray Line File System
 * Copyright (C) 2022 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 * Copyright (C) 2022 Kelsie A. Edie <kelsie.edie@westpoint.edu>
 * Copyright (C) 2022 Jacob A. Huckelberry <jacob.huckelberry@westpoint.edu>
 * Copyright (C) 2022 Nicholas A. Liebers <nicholas.liebers@westpoint.edu>
 *
 */

#define FUSE_USE_VERSION 31

#include <fuse.h>
#include <libgen.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <utime.h>
#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <assert.h>
#include "./grayfs.h"
#include "./gfs-helper.h"
#include "./pathnames.h"
#include "./utils.h"

#define FALSE 0
#define TRUE 1

/*
 * Define the root of our file system.
 */
// TODO (Phase 6)
//   No change is required here; just notice that root is the top-level
//   directory of the GrayFS file system.
struct gray_fobj root;

/*
 * Command line options
 *
 * We can't set default values for the char* fields here because
 * fuse_opt_parse would attempt to free() them when the user specifies
 * different values on the command line.
 */
static struct options {
	const char *filename;
	const char *contents;
	int show_help;
} options;

#define OPTION(t, p)                           \
    { t, offsetof(struct options, p), 1 }

static const struct fuse_opt option_spec[] = {
	OPTION("-h", show_help),
	OPTION("--help", show_help),
	FUSE_OPT_END
};

/*
 * grayfs_init -- Initializes GrayFS
 */
static void *grayfs_init(struct fuse_conn_info *conn, struct fuse_config *cfg)
{
	cfg->kernel_cache = 1;
	init_fobj(&root, GrayDir, "/");
	printf("GrayFS Up and Running!\n");
	return NULL;
}

/*
 * grayfs_getattr - Returns file attributes
 *
 * The stat structure is defined in detail in the stat(2) manual page.
 * For the specified pathname, this function should fill in the elements
 * of the stat structure. If a field is meaningless in the filesystem you
 * are building (e.g., st_ino), then it should be set to 0 or given a
 * "reasonable" value. This function is absolutely required for your file
 * system to run. It is called very, very frequently!
 *
 * Returns:
 *           0, if successful
 *     -ENOENT, if file object for path does not exist
 *
 * Note: We use a simplified getattr. See comments in TODO.
 */
static int grayfs_getattr(const char *path, struct stat *stbuf,
                          struct fuse_file_info *fi)
{
	// TODO (Phase 6) 
	// Find the gray_fobj associated with path using gray_child helper function
	// Fill in stbuf with its stat information using gray_stat helper function
	char cur_path[GRAY_MAX_PATHLENGTH]; 
	strncpy(cur_path,path,GRAY_MAX_PATHLENGTH); 

	struct gray_fobj *cur_gray_fobj = gray_child(&root, cur_path); 
	
	if (cur_gray_fobj == NULL) return -ENOENT; //PATH DOES NOT EXIST

	else{
		gray_stat(cur_gray_fobj, stbuf); 
		printf("getattr: %s\n", path);
		return 0; 
	}
}

/*
 * grayfs_access - Checks whether the calling process can access the path.
 */
int grayfs_access(const char* path, int mask) {
	// Phase 6: This function is optional.
	printf("grayfs_access: %s\n", path);
	return 0;
}

/***********************
 *****             *****
 ***** DIRECTORIES *****
 *****             *****
 ***********************/

/*
 * grayfs_opendir - Opens a directory for reading
 */
int grayfs_opendir(const char* path, struct fuse_file_info* fi) {
	// Phase 6: This function is optional.
	printf("grayfs_opendir: Opening dir *%s*\n", path);
	return 0;
}

/*
 * grayfs_mkdir - Create a directory of the given name with the specified mode
 *
 * See the mkdir(2) man page for details
 * This function is required for any reasonable read-write file system
 */
int grayfs_mkdir(const char *path, mode_t mode) {
	// TODO (Phase 6)
	char * parent; 
	char * child; 
	char ppath[GRAY_MAX_PATHLENGTH]; 
	char cpath[GRAY_MAX_PATHLENGTH]; 
	char copypath[GRAY_MAX_PATHLENGTH];

	strncpy(ppath, path, GRAY_MAX_PATHLENGTH); 
	strncpy(cpath, path, GRAY_MAX_PATHLENGTH); 

	parent = gray_dirname(ppath); 
	child = gray_basename(cpath);

	struct gray_fobj *parent_obj = getFileObject(&root, parent);

	strncpy(copypath, path, GRAY_MAX_PATHLENGTH);

	if (getFileObject(&root, copypath) != NULL) return -EEXIST; // Directory already exists

	struct gray_fobj *child_obj = malloc(sizeof(struct gray_fobj));

	init_fobj(child_obj, GrayDir, child);
	gray_insert(parent_obj, child_obj);

	return 0;
}


/*
 * grayfs_rmdir - Remove the directory of the given name
 *
 * See the rmdir(2) man page for details
 * This function is required for any reasonable read-write file system.
 * It should succeed ONLY if the directory is empty except for "." & "..".
 */
int grayfs_rmdir(const char *path) {
	// TODO (Phase 6)
	char newPath[GRAY_MAX_PATHLENGTH]; 

	strncpy(newPath, path, GRAY_MAX_PATHLENGTH); 

	struct gray_fobj *obj = getFileObject(&root, newPath);

	if (obj == NULL) return -ENOENT; // Directory does not exists
	if (obj->type != GrayDir) return -ENOTDIR; // Not a Directory
	if (obj->children != NULL) return -ENOTEMPTY; // Directory is not empty

	gray_remove(obj);

	return 0;
}



/*
 * grayfs_readdir - Return one or more directory entries (fuse.Direntry)
 * This is one of the most complex FUSE functions.
 * This function is related to the readdir(2) and getdents(2) system
 * calls, as well as the readdir(3) library function.
 * This function is required for essentially any file system because
 * it is needed to make things like "ls" function.
 *
 * FUSE provides a "filler" function that helps you put things into the
 * buffer. Here's the declaration:
 *     int filler(void *buf, char *component, NULL, 0, 0)
 * You should always provide NULL, 0, 0 as the final three arguments.
 * Don't forget that YOU have to put . and .. into the buffer if the
 * object is a directory.
 */

static int grayfs_readdir(const char *path, void *buf, fuse_fill_dir_t filler,
                          off_t offset, struct fuse_file_info *fi,
                          enum fuse_readdir_flags flags)
{
    // TODO (Phase 6)
    // Ignore the 'flags' parameter
    // Always send a zero to the filler function's offset
    char ppath[GRAY_MAX_PATHLENGTH]; 
	char cpath[GRAY_MAX_PATHLENGTH];

    strncpy(ppath, path, GRAY_MAX_PATHLENGTH); 
	strncpy(cpath, path, GRAY_MAX_PATHLENGTH); 


    struct gray_fobj *parent_obj = getFileObject(&root, ppath);

	if (parent_obj == NULL) return -ENOENT; // No such file or directory

    if (parent_obj->type == GrayDir){
		filler(buf, ".", NULL, 0, 0);
        filler(buf, "..", NULL, 0, 0);
		if (parent_obj->children == NULL){ // No children, terminate
			return 0;
		}
        filler(buf, parent_obj->children->name, NULL, 0, 0);
    }

	if (parent_obj->type == GrayFile) return -ENOTDIR; // Is this a possible behavior?

    else if (NULL != parent_obj->children->sibling){ // Recursively move through directory
        struct gray_fobj *sib_obj = parent_obj->children->sibling; 
        
		while(NULL != sib_obj){
            filler(buf, sib_obj->name, NULL, 0, 0);
            sib_obj = sib_obj->sibling;
        }
    }

    printf("grayfs_readdir: *%s*\n", path);
    return 0; 
}

/*************************
 *****               *****
 ***** REGULAR FILES *****
 *****               *****
 *************************/

/*
 * grayfs_create - Creates a file object named path with the given mode
 * See the creat(2) man page for details.
 */
int grayfs_create(const char *path, mode_t mode, struct fuse_file_info *fi) {
	// TODO (Phase 6)
	char path1[GRAY_MAX_PATHLENGTH];
	char path2[GRAY_MAX_PATHLENGTH];
	char path3[GRAY_MAX_PATHLENGTH];

	strncpy(path1, path, GRAY_MAX_PATHLENGTH);
	strncpy(path2, path, GRAY_MAX_PATHLENGTH);
	strncpy(path3, path, GRAY_MAX_PATHLENGTH);

	char * parentStr = gray_dirname(path1); 
	char * baseStr = gray_basename(path2);

	if (getFileObject(&root, path3) != NULL) return -EEXIST; // File object already exists

	struct gray_fobj *newFile = malloc(sizeof(struct gray_fobj));
	init_fobj(newFile, GrayFile, baseStr);
	newFile->mode = mode;
	struct gray_fobj *parent = getFileObject(&root, parentStr);

	if (NULL == parent) return -ENOENT; // There is no parent

	gray_insert(parent, newFile);

	printf("grayfs_create: %s\n", path);
	return 0;
}

/*
 * grayfs_truncate - Truncates the file object named path to the specified size
 * See the truncate(2) man page for details.
 */
static int grayfs_truncate(const char *path, off_t size,
                           struct fuse_file_info *fi)
{
	// TODO (Phase 6)
	// Investigate with Jacob if this is working properly
	char trunc_path[GRAY_MAX_PATHLENGTH];
	strncpy(trunc_path, path, GRAY_MAX_PATHLENGTH);

	struct gray_fobj *trunc_file = getFileObject(&root, trunc_path);
	if (NULL == trunc_file || trunc_file->type != GrayFile) return -ENOENT; // If file does not exist or type is not a file
	gray_truncate(trunc_file, size);
	printf("truncate: path:%s size:%d\n", path, (int)size);
	return 0;
}

/*
 * grayfs_open - Opens the file object named path
 * See open(2) man page for details.
 */
static int grayfs_open(const char *path, struct fuse_file_info *fi) {
	// TODO (Phase 6)
	/*
	 * Note: A real file system would check that the open flags in
	 * the system call request are permitted based on the mode of
	 * the file. Our simple file system will omit this check, though
	 * there might be bonus points available to you if you do
	 * implement this feature.
	 */
	char open_path[GRAY_MAX_PATHLENGTH];
	strncpy(open_path, path, GRAY_MAX_PATHLENGTH);
	struct gray_fobj *open_file = getFileObject(&root, open_path);
	if (NULL == open_file) return -ENOENT; // If file does not exist

	printf("grayfs_open: path:%s\n", path);
	return 0;
	// Below is repeats what is above ^.
	// If NULL, then it will break.
	// Therefore, it will always NOT be NULL by this point.
	/*
	if (NULL != open_file){
		return 0;
	}
	*/
}

/*
 * grayfs_read - Reads from a file
 * See read(2) man page for details.
 */
static int grayfs_read(const char *path, char *buf, size_t size, off_t offset,
                       struct fuse_file_info *fi)
{
	// TODO (Phase 6)
	char read_path[GRAY_MAX_PATHLENGTH];
	strncpy(read_path, path, GRAY_MAX_PATHLENGTH);
	struct gray_fobj *read_file = getFileObject(&root, read_path);
	if (read_file == NULL) return -ENOENT; // If file does not exist, cannot read

	buf = gray_read(read_file, offset, read_file->length, buf);

	printf("grayfs_read: path:%s size:%d, offset: %d\n", path, (int)size, (int)offset);
	return read_file->length; 
}

/*
 * grayfs_write - Writes to the file named path size bytes from the buf buffer
 * See write(2) man page for details.
 */
static int grayfs_write(const char *path, const char *buf, size_t size,
                        off_t offset, struct fuse_file_info *fi) {
	// TODO (Phase 6)
	char write_path[GRAY_MAX_PATHLENGTH];
	char new_buf[GRAY_MAX_FILESIZE];

	strncpy(write_path, path, GRAY_MAX_PATHLENGTH);
	strncpy(new_buf, buf, size);

	struct gray_fobj *write_file = getFileObject(&root, write_path);
	if (NULL == write_file) return -ENOENT; // if file doesn't exist, cannot write
	int output = gray_write(write_file, offset, new_buf); // no error but requires char * for buff
	// printf("%d\n", write_file->length);
	printf("grayfs_write: path:%s size:%d offset: %d buf=%s\n", path, (int)size, (int)offset, buf);
	return output;
}

/*
 * grayfs_unlink - Removes the file object named path
 * See unlink(2) man page for details
 */
static int grayfs_unlink(const char *path) {
	// TODO (Phase 6)
	char pathCpy[GRAY_MAX_PATHLENGTH];
	strncpy(pathCpy, path, GRAY_MAX_PATHLENGTH);

	struct gray_fobj * tempFile = getFileObject(&root, pathCpy);

	if (NULL == tempFile) return -ENOENT; // File to remove does not exist

	if (tempFile->mode == GrayDir) return -EISDIR; // Cannot remove a directory with this function

	gray_remove(tempFile);

	printf("grayfs_unlink: path:%s\n", path);
	return 0;
}

/*
 * grayfs_rename - Renames a file within a single directory.
 * See the rename(2) man page for details.
 *
 * Note:
 * The rename(2) command is quite complex. The grayfs implementation need only
 * support the special case where from and to paths have the same parent.
 */
static int grayfs_rename(const char *from, const char *to, unsigned int flags) {
	// TODO (Phase 6)
	char pathCpy[GRAY_MAX_PATHLENGTH];
	char toCpy[GRAY_MAX_PATHLENGTH];

	printf("from: %s, to: %s\n", from, to);
	strncpy(pathCpy, from, GRAY_MAX_PATHLENGTH);
	strncpy(toCpy, to, GRAY_MAX_PATHLENGTH);
	char * renamedFile = gray_basename(toCpy);
	
	struct gray_fobj * file = getFileObject(&root, pathCpy);
	if (NULL == file) return -ENOENT; // Ensures from exists

	struct gray_fobj * toFile = getFileObject(&root, toCpy);
	if (toFile != NULL) return EEXIST; // Ensures that to does not exist
	
	
	strncpy(file->name, renamedFile, GRAY_NAME_SIZE);



	printf("grayfs_rename: from:%s to:%s flags:%d\n", from, to, flags);
	return 0;
}

/*********************************
 *****                       *****
 ***** SPECIAL FILES & LINKS *****
 *****                       *****
 *********************************/


/*
 * grayfs_mknod - Create a special (device) file, FIFO, or socket
 * See the mknod(2) man page for details
 * Ignore the dev number.
 */
static int grayfs_mknod(const char *path, mode_t mode, dev_t rdev) {
	// TODO (Phase 6)
	char path1[GRAY_MAX_PATHLENGTH];
	char path2[GRAY_MAX_PATHLENGTH];

	strncpy(path1, path, GRAY_MAX_PATHLENGTH);
	strncpy(path2, path, GRAY_MAX_PATHLENGTH);

	char * parentStr = gray_dirname(path1); 
	char * child = gray_basename(path2);

	struct gray_fobj *newFile = malloc(sizeof(struct gray_fobj));
	
	init_fobj(newFile, GrayDev, child);
	newFile->mode = mode;
	struct gray_fobj *parent = getFileObject(&root, parentStr);
	if (parent == NULL) return -ENOENT; 

	gray_insert(parent, newFile);
	printf("grayfs_mknod: path:%s mode:%d, dev: %d\n", path, (int)mode, (int)rdev);
	return 0;
}

/*
 * grayfs_link - Create a link (also known as a hard link) to an existing file.
 *
 * Hard links are NOT supported by grayfs.
 * Implementation of hard links is non-trivial and not required for Phase 6.
 */
static int grayfs_link(const char *from, const char *to) {
	// NOT REQUIRED
	printf("grayfs_link: from:%s to:%s\n", from, to);
	return -ENOTSUP;
}

/*
 * grayfs_symlink - Create a symbolic link (also known as a symlink)
 * See the symlink(2) man page for details.
 * A symlink is a pathname to the file you are linking to (aliasing)
 * It creates a file that simply points to the other file in memory...
 */
static int grayfs_symlink(const char *from, const char *to) {
	// TODO (Phase 6)
	char fromCpy[GRAY_MAX_PATHLENGTH];
	char toCpy[GRAY_MAX_PATHLENGTH];
	char toCpy1[GRAY_MAX_PATHLENGTH];

	strncpy(fromCpy, from, GRAY_MAX_PATHLENGTH);
	strncpy(toCpy, to, GRAY_MAX_PATHLENGTH);
	strncpy(toCpy1, to, GRAY_MAX_PATHLENGTH);

	char * parentLinkedName = gray_dirname(toCpy); 
	char * linkedName = gray_basename(toCpy1);


	struct gray_fobj * parent = getFileObject(&root, parentLinkedName);
	if (NULL == parent) return -ENOENT; // If parent does not exist
	struct gray_fobj *linkedFile = malloc(sizeof(struct gray_fobj));
	
	init_fobj(linkedFile, GrayLink, linkedName);

	strncpy(linkedFile->content, fromCpy, GRAY_MAX_FILESIZE); // Put from path into the linkedfile content

	gray_insert(parent, linkedFile);


	printf("grayfs_symlink: from:%s to:%s\n", from, to);
	return 0;
}

/*
 * grayfs_readlink - Return the target of a symbolic link
 * See the readlink(2) man page for details.
 */
static int grayfs_readlink(const char *path, char *buf, size_t size) {
	// TODO (Phase 6)
	char read_path[GRAY_MAX_PATHLENGTH];
	strncpy(read_path, path, GRAY_MAX_PATHLENGTH);

	struct gray_fobj *read_file = getFileObject(&root, read_path);
	if (NULL == read_file) return -ENOENT; // In theory this should not occur, but prevents NULL pointer exception
	strncpy(buf, read_file->content, GRAY_MAX_FILESIZE); // <-- fixed to prevent reading from outside of the buffer
	printf("grayfs_readlink: path:%s size:%d\n", path, (int)size);
	printf("%s\n", buf);
	return 0;
}

/*********************************
 *****                       *****
 ***** ACCESS and ATTRIBUTES *****
 *****                       *****
 *********************************/

/*
 * grayfs_chmod - Change the mode (aka permissions) of the file object
 * See chmod(2) man page for details.
 */
static int grayfs_chmod(const char *path, mode_t mode,
                        struct fuse_file_info *fi)
{
	// TODO (Phase 6)
	char pathCpy[GRAY_MAX_FILESIZE]; 
	strncpy(pathCpy, path, GRAY_MAX_FILESIZE); 

	struct gray_fobj * file = getFileObject(&root, pathCpy);

	if (NULL == file) return -ENOENT; // if no file exists
	
	file->mode = mode; 

	printf("grayfs_chmod: path:%s mode:%d\n", path, (int)mode);

	return 0;
}

/*
 * grayfs_chown - Change the owner and group of the file object
 * See chown(2) man page for details.
 */
static int grayfs_chown(const char *path, uid_t uid, gid_t gid,
                        struct fuse_file_info *fi)
{
	// TODO (Phase 6)
	char pathCpy[GRAY_MAX_FILESIZE]; 
	strncpy(pathCpy, path, GRAY_MAX_FILESIZE); 

	struct gray_fobj * file = getFileObject(&root, pathCpy);

	if (NULL == file) return -ENOENT;
	
	file->user_id = uid; 
	file->group_id = gid; 
	
	printf("grayfs_chown: path:%s uid:%d, gid: %d\n", path, (int)uid, (int)gid);
	return 0;
}

/*
 * grayfs_utimens - Update the last access and modification times of the file
 * See the utime(2) man page for details.
 */
int grayfs_utimens(const char *path, const struct timespec tv[2],
                   struct fuse_file_info *fi) {
	// TODO (Phase 6)
	char time_path[GRAY_MAX_PATHLENGTH];

	strncpy(time_path, path, GRAY_MAX_PATHLENGTH);

	struct gray_fobj *time_file = getFileObject(&root, time_path);
	if (NULL == time_file) return -ENOENT; // if file at path does not exist
	updateTimes(time_file, true, true, false);
	printf("grayfs_utimens: %s\n", path);
	return 0;
}

/*
 * This structure is used by the FUSE library much like the system call
 * table in the system call handler in Pintos to figure out which
 * functions know how to handle which file system requests.
 */
static const struct fuse_operations grayfs_oper = {
	.init       = grayfs_init,
	.getattr	= grayfs_getattr,
	.access     = grayfs_access,
	.opendir    = grayfs_opendir,
	.mkdir      = grayfs_mkdir,
	.rmdir      = grayfs_rmdir,
	.readdir	= grayfs_readdir,
	.create     = grayfs_create,
	.truncate   = grayfs_truncate,
	.open		= grayfs_open,
	.read		= grayfs_read,
	.write      = grayfs_write,
	.unlink     = grayfs_unlink,
	.rename     = grayfs_rename,
	.mknod      = grayfs_mknod,
	.link       = grayfs_link,
    .symlink    = grayfs_symlink,
	.readlink   = grayfs_readlink,
	.chown      = grayfs_chown,
	.chmod      = grayfs_chmod,
	.utimens    = grayfs_utimens,
};

static void showUsageMessage(const char *programName)
{
	printf("Usage: %s [options] <mountpoint>\n\n", programName);
	printf("FUSE supported options:");
	printf("  -d runs in debug mode\n");
	printf("  -s runs with a single thread (highly recommended for CS481)\n");
	printf("  -f runs in the foreground (highly recommended for CS481)\n");
	printf("\n");
}

/*
 * Phase 6
 * The main function has been written for you. No changes required.
 */
int main(int argc, char *argv[])
{
	int ret;
	struct fuse_args args = FUSE_ARGS_INIT(argc, argv);

	printf("Grayfs Booting...\n");

	/* Parse options */
	if (fuse_opt_parse(&args, &options, option_spec, NULL) == -1)
		return 1;

	/* Show help messages. */
	if (options.show_help) {
		showUsageMessage(argv[0]);
		assert(fuse_opt_add_arg(&args, "--help") == 0);
		args.argv[0][0] = '\0';
	}

	ret = fuse_main(args.argc, args.argv, &grayfs_oper, NULL);
	fuse_opt_free_args(&args);

	return ret;
}
