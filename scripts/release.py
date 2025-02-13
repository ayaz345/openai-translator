import subprocess
from functools import reduce

def get_current_version_from_tag():
    subprocess.check_output(['git', 'pull', 'origin', 'main', '-r'])
    subprocess.check_output(['git', 'fetch', '--tags'])
    """Get the current version from the latest tag in the repository."""
    # Get the latest tag in the repository.
    tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode('utf-8').strip()
    return tag.lstrip('v')

def generate_new_version():
    """Generate the new version for the current release."""
    # Get the current version.
    previous_version = get_current_version_from_tag()
    # Get the new version.
    new_version = previous_version.split('.')
    new_version[-1] = str(int(new_version[-1]) + 1)
    new_version = '.'.join(new_version)
    # Return the new version.
    return new_version

def generate_release_note():
    """Generate the release note for the current version."""
    # Get the current version.
    previous_version = get_current_version_from_tag()
    return (
        subprocess.check_output(
            ['git', 'log', '--pretty="%s"', f'v{previous_version}..HEAD']
        )
        .decode('utf-8')
        .strip()
    )

def create_new_tag():
    """Create a new tag for the current release."""
    # Get the current version.
    new_version = generate_new_version()
    release_note = generate_release_note()

    release_notes = []
    seen = set()
    for line in release_note.split('\n'):
        line = line.strip().strip('"')
        t_, _, _ = line.partition(':')
        if t_.lower() not in ('fix', 'feat', 'docs', 'refactor', 'optimize'):
            continue
        if line in seen:
            continue
        release_notes.append(line)
        seen.add(line)
    args = ['git', 'tag', '-a', f'v{new_version}'] + flatten(
        [['-m', line] for line in release_notes]
    )
    # Create a new tag for the current release.
    subprocess.check_output(args)
    # Push the new tag to the repository.
    subprocess.check_output(['git', 'push', 'origin', f'v{new_version}'])

def flatten(l):
    return l if not l else reduce(lambda x, y: x + y, l)

def main():
    print(create_new_tag())

if __name__ == '__main__':
    main()
