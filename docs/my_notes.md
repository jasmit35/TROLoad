# Mounting an NFS Share

To mount an NFS share, you can use the following command

```bash
 mount -t nfs -o hard 192.168.1.70:/volume4/NFSStorage /mnt/nfsstorage
```

## Explanation

- `sudo`: Runs the command with superuser privileges.
- `mount`: Command to mount a filesystem.
- `-t nfs`: Specifies the type of filesystem as NFS.
- `192.168.1.70:/Volume4/NFSStorage`: The NFS server and the shared directory.
- `/mnt/nfsstorage`: The local directory where the NFS share will be mounted.

## Notes

- Ensure the `/mnt/nfsstorage` directory exists before running the command.
- Verify that the NFS server is accessible and properly configured.
- You may need to install the NFS client utilities on your system if not already installed.

## Unmounting

To unmount the NFS share, use:

```bash
sudo umount /mnt/nfsstorage
```

## I give up

sudo mkdir /Volumes/nfsstorage/
sudo mount -t nfs -o vers=4,resvport,rw 192.168.1.70:/volume4/NFSStorage /Volumes/nfsstorage/
