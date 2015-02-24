'''
   Copyright 2015 Kendall Bailey

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
#!/bin/bash

IFS=$'\n' read -d '' -r -a lines < reviewedApps2.txt
for l in "${lines[@]}"
do
	rm "reviewFiles/"${l}".json"
done
echo "Done cleaning up old reviews"
