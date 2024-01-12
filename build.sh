entry="main.py"
output="TermGecko.py"


while getopts e:o: OPT
do
    case $OPT in 
        "e" ) entry=${OPTARG};;
        "o" ) output=${OPTARG};;
    esac
done

if ! [ -d "build" ]; then
    mkdir build
fi

if ! command -v stickytape &> /dev/null
then
    echo "stickytape is not installed, installing now..."
    pip install stickytape
fi

stickytape ${entry} > "build/${output}"

echo "Build Success"