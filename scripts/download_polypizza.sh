#!/bin/bash
# Download pig models from poly.pizza
# Usage: ./download_polypizza.sh

OUTDIR="/home/turtle_wolfe/repos/Auto-Blender/models/polypizza"
mkdir -p "$OUTDIR"

# List of pig model IDs from poly.pizza search
# Format: "ID|name|author|license"
MODELS=(
    "6XC3XssJIU_|pig_poly_google_1|Poly by Google|CC-BY"
    "brcb6xLELnz|pig_poly_google_2|Poly by Google|CC-BY"
    "6yc3isbjZST|pig_poly_google_3|Poly by Google|CC-BY"
    "TNvG3QUFlp|pig_quaternius_1|Quaternius|CC-BY"
    "u35l6uP5vj|pig_quaternius_2|Quaternius|CC-BY"
    "bbPhEBl5Bh0|pig_jeremy|jeremy|CC-BY"
    "57fSWum6F1P|boar_poly_google|Poly by Google|CC-BY"
    "5CHg_vV9IJH|hog_aya_kawa|Aya Kawa|CC-BY"
    "abovMDkoWAN|voxel_pig_mauri|Mauri Helme|CC-BY"
    "dpvS2kdW6I9|piggy_bank_poly_google|Poly by Google|CC-BY"
    "d1lUL18me4S|piggy_bank_poly_google_2|Poly by Google|CC-BY"
    "1KAexv0Erv|piggy_bank_creativetrio|CreativeTrio|CC-BY"
    "3eoOcw_d00X|collared_peccary|Poly by Google|CC-BY"
)

SUCCESS=()
FAILED=()

for entry in "${MODELS[@]}"; do
    IFS='|' read -r id name author license <<< "$entry"
    outfile="$OUTDIR/${name}.glb"
    
    echo "Downloading $name ($author)..."
    
    if curl -sL -o "$outfile" "https://poly.pizza/api/download/$id/glb" 2>/dev/null; then
        # Check if file is valid (not an error page)
        filesize=$(stat -f%z "$outfile" 2>/dev/null || stat -c%s "$outfile" 2>/dev/null)
        if [ "$filesize" -gt 1000 ]; then
            echo "  OK: $filesize bytes"
            SUCCESS+=("$name|$author|$license|$filesize")
        else
            echo "  FAILED: File too small ($filesize bytes)"
            FAILED+=("$name|$author|$id|small_file")
            rm -f "$outfile"
        fi
    else
        echo "  FAILED: curl error"
        FAILED+=("$name|$author|$id|curl_error")
    fi
done

echo ""
echo "=========================================="
echo "DOWNLOAD SUMMARY"
echo "=========================================="
echo ""
echo "SUCCESS (${#SUCCESS[@]}):"
for s in "${SUCCESS[@]}"; do
    IFS='|' read -r name author license size <<< "$s"
    echo "  $name ($author) - $license - $size bytes"
done

echo ""
echo "FAILED (${#FAILED[@]}):"
for f in "${FAILED[@]}"; do
    IFS='|' read -r name author id reason <<< "$f"
    echo "  $name ($author) - ID: $id - Reason: $reason"
done

echo ""
echo "Files saved to: $OUTDIR"
