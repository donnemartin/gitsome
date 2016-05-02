_gh_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _GH_COMPLETE=complete $1 ) )
    return 0
}

complete -F _gh_completion -o default gh;
