BEGIN {
    FS = "(:.*?)?##";
    previous_line_was_target=-1;

    print "Choose one of the following targets:"
}
{
    if ($1 == "") {
        if (previous_line_was_target != 0) {
            printf "\n";
        }

        gsub(/^[ \t]+|[ \t]+$/, "", $2);
        printf "\033[1m%s\033[0m\n", $2;

        previous_line_was_target=0;
    } else {
        if (previous_line_was_target == 0) {
            printf "\n";
        }

        printf "\033[36m%-40s\033[0m %s\n", $1, $2;

        previous_line_was_target=1;
    }
}
