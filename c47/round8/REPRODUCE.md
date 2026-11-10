# Reproduce the release

Python 3 and its standard library suffice. Run from this folder without disabling assertions, one process at a time at nice 10. Use a copy to preserve the shipped timing-bearing receipts and checksums.

```sh
export PYTHONDONTWRITEBYTECODE=1
/usr/bin/time -l nice -n 10 python3 verify_exact.py certificates/final.json --claim 114388018195906255044427129545533845966664904690010061034899/67069990589546886330812144279013633721316147200000000000000 --out release_validation/exact.json
/usr/bin/time -l nice -n 10 python3 rejection_controls.py certificates/final.json 114388018195906255044427129545533845966664904690010061034899/67069990589546886330812144279013633721316147200000000000000
/usr/bin/time -l nice -n 10 python3 finite_instance.py certificates/final.json release_validation/exact.json release_validation/finite.json --claim 4263755563/2500000000
(cd referee && /usr/bin/time -l nice -n 10 python3 referee_check.py)
/usr/bin/time -l nice -n 10 python3 comparison.py
/usr/bin/time -l nice -n 10 python3 sources/claim_facts.py
```

The seven controls must reject: raised claim, changed heavy mass, oversized radius, expanded rectangle, atom outside cell, zero mass and duplicate atom. They generate corrupted certificate files under certificates/controls/final. The release omits these regenerable files; their SHA-256 values and the generation command are in release_validation/omitted-generated.json. Remove the generated folder with `/usr/bin/trash certificates/controls` after replay. The referee checker produces a regenerable per-witness table; its original hash is in referee/README.md and its replay hash in release_validation/omitted-generated.json. The table is omitted from the package.

The referee checker reads only the certificate and finite-instance data, not producer code. The source calculation summary is referee/exact_results.json; its fresh replay is release_validation/referee-results.json. REPLAY.json records hashes of the publication copies of the supplied historical mathematical inputs. The release PROOF.md changes citation and review-status wording; the supplied producer-proof.md is retained byte-for-byte under referee/sources/.

The finite block is specified by formula, without expanding its atoms. Floats and decimal fields are display only. The written proof supplies the passage to the planar L1 constant; no formalization or human peer review is claimed. Numerical search is unnecessary for replay and is outside this frozen-certificate release.

For the unchanged shipped bytes, run:

```sh
shasum -a 256 -c SHA256SUMS
```

## Unpublished search history

The following superseded certificates, identical snapshot aliases and archives are unpublished search history, omitted and unnecessary for replay. No full-family producer or enumeration is needed. Run the four replays serially; stop a process exceeding 8 GB resident memory.

- certificates/best.json: SHA-256 `318370e5c50761632ad4e32bc68792c02bd14b1d789c5125dd4908b02dab16dd`.
- certificates/best_1.70550222&#53;2192482.json: SHA-256 `1afaf5d5c8968fffd3f98cf77de4d462dd1070b9dea4ec1456dd5a91087bfb44`.
- certificates/checkpoints-1794317376.tar.xz: SHA-256 `e16d0d94caf78dad3aaacfe96dc7d18178885166ce00e10caacc39c8674ad674`.
- certificates/checkpoints-curve-1794316883.tar.xz: SHA-256 `aa17ec86d4b519714e0eadbba459cc4800dae868a4df97c569c928977c94f51e`.
- certificates/checkpoints-final-1794317635.tar.xz: SHA-256 `eda612bb89deb05ac10a24a0be2a05b59a7d58cf1f01e5e6171b1161917a6b20`.
- certificates/checkpoints-final-1794317779.tar.xz: SHA-256 `474012ffb2f6ba90f796e210987dbadea5a902078ccd122b4dd7ad1b4d541351`.
- certificates/final-controls.tar.xz: SHA-256 `e014402f070b815c5327273400d341d0f4930846730d223beb9bcba5bb64f29b`.
- certificates/full-family-comparisons-2.tar.xz: SHA-256 `781c5161c68f0ff37286d2a62ca3a955683fdefaf6bb4e25a3a12e6d8ce57684`.
- certificates/full-family-comparisons.tar.xz: SHA-256 `dc29794c866fbec914490eeac6bde73aaa2f8dc6bdd2390022105c6ea252da2c`.
- certificates/provisional-controls.tar.xz: SHA-256 `41e76a966af91ec193059b297b1584eb36b1f5228684941fe228f26bfae4d035`.
- certificates/start454.json: SHA-256 `0cd5cc0954f8cc01ac1184b7cf095ce22bb3cdaa9a602fe25c20d8c1bd2bfe04`.
- chains/final-working-snapshots-1794317649.tar.xz: SHA-256 `20aa152c20fb7ff379a145a6ca6edba5c642d596c8faac52b6d80df4e265caed`.
- chains/final-working-snapshots-1794317783.tar.xz: SHA-256 `13589e1799fcf44ccb76524a0a30078c28c36cfb856f319764c71454c635138d`.
- chains/working-history-1794299841.tar.xz: SHA-256 `65d360347e6609fbd63538d2863cad8aa9826c49289b35b6d9dca66225c7f234`.
- chains/working-history-1794299972.tar.xz: SHA-256 `799d6dc20ac2606d22f916bc1ecd4c18c94096f65eda5054b0a5ebf4ff2fa7ca`.
- chains/working-history-1794300105.tar.xz: SHA-256 `b5394041a1a7e0f09b18f977831716adaa5b263840cdf6292545b0dfbe49dd7a`.
- chains/working-history-1794300364.tar.xz: SHA-256 `5b946d441553462b199135e0a35e5f976ced67bc4f3b61d02ddd6bfa077a9341`.
- chains/working-history-1794300503.tar.xz: SHA-256 `3f9cfdc06166b1657d67f17555e14c4f287bef617727dc9a8b6846f2556998c2`.
- chains/working-history-1794301299.tar.xz: SHA-256 `64c2049d76fe136637c514281c09de68128463922e90055b3a217f4c75d572a1`.
- chains/working-history-1794302073.tar.xz: SHA-256 `1d622b3657c8cbd6bbc948a1ce4c4501a5eccd5c50ffd688b9234cd6538a3a2b`.
- chains/working-history-1794303091.tar.xz: SHA-256 `f2d28053bfaa6bcf4d99704baa724e7f1e520f575a3b49641251e8ca990635e2`.
- logs/helper-history-1794299656.tar.xz: SHA-256 `dd94112627414b5a49b9929b4d4ec53091d556438cbf8f5381a8ad6f6c0c827b`.
- logs/helper-history-1794299778.tar.xz: SHA-256 `9231c985723eb2f2f4d759927629ed5abe91e4dc283fba3230f06f1236e806b6`.
- logs/helper-history-1794301690.tar.xz: SHA-256 `773f921e904c9f5211d298ffe628997814f23ddf3a5b0986882bdbe114b714e8`.
- logs/helper-history-1794301812.tar.xz: SHA-256 `391cddeb6468298bc87d6d7c6e6db774f786afd261898720dcae30e911f5169c`.
- logs/helper-history-1794301945.tar.xz: SHA-256 `a9c2171776159f995f5186d602280b597ee2f96a9564dadc9bd77e0964f2aa3e`.
- logs/helper-history-1794302073.tar.xz: SHA-256 `8ef2192047ca882aeafda9a324cf6ebff529fae0ae7a23a61c231faca53d4b77`.
- logs/helper-history-1794302197.tar.xz: SHA-256 `3526ef13233fad26e14f7c20166d23e163a3b6b2de97dace87bef0a958deb472`.
- logs/helper-history-1794302320.tar.xz: SHA-256 `cfb86b92bc5cc2103767cf31883b4b147af686d62f407735cedde4183604e3ce`.
- logs/helper-history-1794302442.tar.xz: SHA-256 `31bb7ed936c1f5ee3a98c926e8c2644d84b8c2240c8b58385a35fe33d49acd4f`.
- logs/helper-history-1794302579.tar.xz: SHA-256 `41f68e08e4a6de7a9866032b4a9b9902e7c423204c5c7bbfe4cbbd9ec6d9dfda`.
- logs/helper-history-1794302716.tar.xz: SHA-256 `20eec84877ae88e37e544e991f5ce03d11cc9c2275d097115aeba68076d06477`.
- logs/helper-history-1794302839.tar.xz: SHA-256 `0387939d450b666bffb4d395ee87fa53e3d818dd14d3b5551b5b19427b3c2d96`.
- logs/helper-history-1794302969.tar.xz: SHA-256 `0ee7b018d4632874387c8944fe223ee9cccac5bd944284abe6e71ef00c360405`.
- logs/helper-history-1794303091.tar.xz: SHA-256 `e9742002cb771b7e8cf2f46bcee49a36d51a030566d45333e0242c2b2fbf6c13`.
- logs/helper-history-1794303212.tar.xz: SHA-256 `3a82ec5f4b2a6ac68bf4887c7653ed089bc683a94052fd9ce73c5b5a049f0509`.
- logs/helper-history-1794305140.tar.xz: SHA-256 `c5ebe65d58fe7c68d059b35479b4da3d65ac0550285c08bb8312f7f1065b655d`.
- logs/helper-history-1794305266.tar.xz: SHA-256 `e69dece7522323895a870508a2af10e84561e5b5cbfeac771f740b7f279b1f6c`.
- logs/helper-history-1794305402.tar.xz: SHA-256 `aede0e4aa47a62747166a8dba3a970ee5fdd5720af80a46434ee2c71d7c1afda`.
- logs/helper-history-1794305530.tar.xz: SHA-256 `f576c42211dfad4e018050112836b81997f6c59cbb9b96c69dc966625bbee108`.
- logs/helper-history-1794305652.tar.xz: SHA-256 `8590537090cea2d5d037a9d556e1fa473491c73195eed129baaf842f9160ec91`.
- logs/helper-history-1794305789.tar.xz: SHA-256 `68fd0c2bd101df8d4dc86f7860e9e32d380d23c8f7a9dee1215a4c4e14269201`.
- logs/helper-history-1794305911.tar.xz: SHA-256 `917ce3a41ad499146757ce81f818cbc9e150647b9dfc39583e4653ab46e5af16`.
- logs/helper-history-1794306046.tar.xz: SHA-256 `4bd3ba43b86c2d87bd3367ff2c8fffe8700604b57c9cf86897f19bf0a25e85ae`.
- logs/helper-history-1794306175.tar.xz: SHA-256 `d545adcf529aad01e49c4a2f08446885119c7c90212f0f78204e08f1c3f46479`.
- logs/helper-history-1794306311.tar.xz: SHA-256 `535ff017345921de767b420dd98e4fc7142c9328313f222af8fcf033ea8ce4d3`.
- logs/helper-history-1794306440.tar.xz: SHA-256 `f9543dde2607da736c6348012585d5c64502bfec6ed1221499397ea5f3bf3471`.
- logs/helper-history-1794307150.tar.xz: SHA-256 `7438b0ad77726f046bc5116fa87d44b4cd65681b5e88fbab886f63c3ad24cdd0`.
- logs/helper-history-1794307212.tar.xz: SHA-256 `151e5fff0e0797aa86771cf5a5f706651061d5309cbf4e8065c8c4b96e545fa8`.
- logs/helper-history-1794307369.tar.xz: SHA-256 `4d162d5a2bbb1f9050b3dd75cd2bc99616cbbdd7140f566ed35c38d24dfcc9d0`.
- logs/helper-history-1794307491.tar.xz: SHA-256 `841521213595387ee113ecd0236733d78d9812c95e889e4eb51f0b791a2e8ac8`.
- logs/helper-history-1794307619.tar.xz: SHA-256 `57dbd4fc209cfc5f5b44e57d8c0378ef6ecace638f1a9d00276c1772eab0ef61`.
- logs/helper-history-1794307741.tar.xz: SHA-256 `9b778264c07d0d8a6bf87e60ba445bc3099b86575a126987c96aee7a22e679ab`.
- logs/helper-history-1794307887.tar.xz: SHA-256 `f83f688ef9dbb088f0dcf541e06985cd47f515d13287ecd1807c666acee476f5`.
- logs/helper-history-1794308026.tar.xz: SHA-256 `b6d1249b038ecb93e7bd3c29536f27a77c1cd3ee4c0e35ea5ef94d919868ee49`.
- logs/helper-history-1794308152.tar.xz: SHA-256 `f61d9ba6cb5d6b7561a12a61b078e5095388332d1ca74e38122f2f21648a4074`.
- logs/helper-history-1794308294.tar.xz: SHA-256 `47e708bc6dc36cef0da2531f33d38a277b501bbbe6d58e4facfaa8828433c537`.
- logs/helper-history-1794308434.tar.xz: SHA-256 `1e2ed764131877a74a4a228676697f297873d4c505e38ad584ebd779e816a93f`.
- logs/helper-history-1794308565.tar.xz: SHA-256 `e703c7e103d2903634f94078ac2745ad651c4ecbffba8106765ded316ad18236`.
- logs/helper-history-1794308702.tar.xz: SHA-256 `768c5074804cc9a6f6a4efabd38f812e43dd0582f993e43eb11d3d322509f27a`.
- logs/helper-history-1794308842.tar.xz: SHA-256 `7ea79ae5170f552559a4935625b74acba6575a7c8e4d00f7593c169f85e40674`.
- logs/helper-history-1794308966.tar.xz: SHA-256 `21f7526f1f4543274b4b51fc650ac60d98faca79d1030ef1420f438d3c49518f`.
- logs/helper-history-1794309104.tar.xz: SHA-256 `bcf312f599cbd9516e39dd77dd928ab0fa2ab7c1f36b5db2dd9b14198e1960d0`.
- logs/helper-history-1794309231.tar.xz: SHA-256 `012a2c5716d2170ca16f74973f3e74291b5fc684465af660e0c0bf88b614ab21`.
- logs/helper-history-1794309368.tar.xz: SHA-256 `630d9775d853063f7c1b88cc29ce4e440b391e0d7e793864d85b16a90210d60a`.
- logs/helper-history-1794309503.tar.xz: SHA-256 `fc0e9feeccc5284df3a9320fb10cc16e18b603d40bd6956b76b8343915cc4eff`.
- logs/helper-history-1794309631.tar.xz: SHA-256 `da27ac7d00ead43a44e6558fb735b2f328e698f9a79c41887cb0aabf1d59157a`.
- logs/helper-history-1794309755.tar.xz: SHA-256 `8af75f2988961ff34beeb937271d34d60f7bf832c625619fcc53241db47f7a37`.
- logs/helper-history-1794309897.tar.xz: SHA-256 `a1972852c15d69a609bb2a66dbe75ab037d1da14538e67733d7bea9b37f352b9`.
- logs/helper-history-1794310019.tar.xz: SHA-256 `f9e01eee734ce0668bcc6c158d1d2d3b31a329b0bbff614224aee6af10a85781`.
- logs/helper-history-1794310150.tar.xz: SHA-256 `542c8ea2bacc2d3d08dbf91355dae238ee2656a6e5c42d8967c9256a8eaf9f34`.
- logs/helper-history-1794310281.tar.xz: SHA-256 `2dbd3cce1f2346cfd28bb7f3dd26dcc1b41b68f68ddfa72d6741a9b878d5da3c`.
- logs/helper-history-1794310404.tar.xz: SHA-256 `7a96343fba52f83e60883b355a91a6106fcb6e63a49b27fec869d41ac20ce8a6`.
- logs/helper-history-1794310530.tar.xz: SHA-256 `351eca73756378de99e7f6d298bdd74530f26cc17bb15d34386b2379f4fc93dc`.
- logs/helper-history-1794310671.tar.xz: SHA-256 `6155c91ada00cdf57680ddd40cd71fcc6af45c6d094001311c48b6521abb09d3`.
- logs/helper-history-1794310794.tar.xz: SHA-256 `59e35b0cd9af16513948e79e868b8f862f969cab2d65f892f051d2a810b5ce5d`.
- logs/helper-history-1794310936.tar.xz: SHA-256 `97b8de90d834458869980e40d37661149a47708576904fd2fc65ff8007721a12`.
- logs/helper-history-1794311062.tar.xz: SHA-256 `57167801b1f6b5f639f7ef3771554be2b25587a4b921798bb23ebe356b9e7f0a`.
- logs/helper-history-1794311204.tar.xz: SHA-256 `78ee440d7b80594a62e425acd96b680fb62d98b0a76db9fded452db43366dd0c`.
- logs/helper-history-1794311326.tar.xz: SHA-256 `67557eb335b04b8e36338a9cc516c640fc4fa377888eb7a6b257a549b7b7405d`.
- logs/helper-history-1794311451.tar.xz: SHA-256 `d5e45c2410806ce3d1126edf82711b5680695c86f459b0146d3127a8a1fe17c2`.
- logs/helper-history-1794311573.tar.xz: SHA-256 `d97f117af925f54ad15efa733ff1f55c033ec06ad32180315db4a87ae035a288`.
- logs/helper-history-1794311706.tar.xz: SHA-256 `68f334c1f44d9fd9c0fff1c5179f48c3fd41665924b62b6bcebd3738a751f6da`.
- logs/helper-history-1794311835.tar.xz: SHA-256 `c2095a55c7a02847734f4817e3013bf9d71263aca13197286a0f2e1a4169ef55`.
- logs/helper-history-1794311962.tar.xz: SHA-256 `83ddb7e48099c8088670ce92f5eb3703e316b928a731770afd635930263df960`.
- logs/helper-history-1794312100.tar.xz: SHA-256 `184829930885519aecbc38a865d3144e000ed532c4a6fb9f686269089b5b96f8`.
- logs/helper-history-1794312239.tar.xz: SHA-256 `071ae116bbe594630bc0d07281a9926cd34929a891b049e10dc4d6b97b4aa9b9`.
- logs/helper-history-1794312361.tar.xz: SHA-256 `ce211922bcdef9d6a6124bdc94003aabdb6d80c509c7a6e11fa88d2f7932cd5a`.
- logs/helper-history-1794312490.tar.xz: SHA-256 `d3c2541138e854d51a7a40c0fef948b7a2caaae026b7a38a2255898a7c7bbe4b`.
- logs/helper-history-1794312622.tar.xz: SHA-256 `29ef0a7c81336ee9273dcab1c0752d0883770007c07c593c62bee73d62a2bbc2`.
- logs/helper-history-1794312754.tar.xz: SHA-256 `5f63f2e18c859f3b1ccaf513e785d096bf0218eba7a66ce5727b5d5b25689d6e`.
- logs/helper-history-1794312889.tar.xz: SHA-256 `56ff889237bfe4040480991a209d8f4a1cc6d028d15325e3268f267126815f1d`.
- logs/helper-history-1794313018.tar.xz: SHA-256 `303973b1cb78fc1dbc478633dc7752c0dacb36f93a5d89500448695d00c0bce4`.
- logs/helper-history-1794313155.tar.xz: SHA-256 `ecfc245d0a89dba4458fd60db46ec8ad351df93f64347c973ba6c2f9e3b138bb`.
- logs/helper-history-1794313289.tar.xz: SHA-256 `aa02ca597224600ca8d2b646720485e0974a6c53f91d2ee8005712d817f6c35d`.
- logs/helper-history-1794313411.tar.xz: SHA-256 `d873ca18135da4c4d9fe8f3fde055cb5cffaee2714e2f390c4f5abeb21710c17`.
- logs/helper-history-1794313545.tar.xz: SHA-256 `242969ec41181b47efdc014c973717fa8a587546c2d92a6d706b3099f0354176`.
- logs/helper-history-1794313668.tar.xz: SHA-256 `7141595a621acb605b3caffabd9ba2cc70c201f787fba69d7b15f6b656fc216f`.
- logs/helper-history-1794313799.tar.xz: SHA-256 `5c4cf9ca49ae97a87d5047fa0f9c13fb3c3dfef62b0ea2d8aec62aa5f6a8bd92`.
- logs/helper-history-1794313940.tar.xz: SHA-256 `7db5681fdf0dc8653229dc8c63bf86cd8138b8a1667f7b1f530dbc04ec164442`.
- logs/helper-history-1794314079.tar.xz: SHA-256 `514af7613db3531f8e77992796cf188baa83e2e4e22f12c2b2d5f4df3879472b`.
- logs/helper-history-1794314722.tar.xz: SHA-256 `2bf47394bc11cfb1cf34400f6eba97bb04570225848b34e867300840d143055b`.
- logs/helper-history-1794314877.tar.xz: SHA-256 `0173392d1ed708306cbd58d79dbbf31d200cf08e1d1626a2b6a53a27f82dd500`.
- logs/helper-history-1794315019.tar.xz: SHA-256 `9113df38ee42d9e22a92fbbc06d56dcc44710045ee409e03f284f4a0fd0ccfe8`.
- logs/helper-history-1794315163.tar.xz: SHA-256 `69e3dd70634f107715d463177271bf8780dfc88950be1c42cc324e4a77dac520`.
- logs/helper-history-1794315299.tar.xz: SHA-256 `d78314c92f65dca9324d5b65b1cfd916160dfa3acca4d061ea2d219d78137840`.
- logs/helper-history-1794315435.tar.xz: SHA-256 `34690783487bb245f90da354ec50ebea7b19b50f8d05797af8606146095ce1f7`.
- logs/helper-history-1794315563.tar.xz: SHA-256 `e59e691f2584cf68e31c7c89c2acf87d8f18240e72173e10393bce4c882491a8`.
- logs/helper-history-1794315698.tar.xz: SHA-256 `adfe3b804b6c203348cf1b08c650191dad9bfe1023c29c371c9c20331d8df2fc`.
- logs/helper-history-1794315824.tar.xz: SHA-256 `08010572a577fb936835b48b13f56e2103ec6eba41e8e81239664feee300f34d`.
- logs/helper-history-1794315954.tar.xz: SHA-256 `e50b924ddf9ae0812ac12ab4878ef6ec915acfa4bb9c2943be9a4c8542920e5d`.
- logs/helper-history-1794316089.tar.xz: SHA-256 `cd7d448db5c22bdb8f345b8bad0a40d93638a78c7f435cce9f8656a534f85589`.
- logs/helper-history-1794316225.tar.xz: SHA-256 `c93dd6c5505c1eeb258eaacc6a5c38f7bd87c4301ce00c566bfbfb6d788885d7`.
- logs/helper-history-1794316352.tar.xz: SHA-256 `651f75f5089011ac9371de1a0ef4ad2b6f9a251b1c70cde1d6cbbf8e3eef10dc`.
- logs/helper-history-1794316490.tar.xz: SHA-256 `a4941f1a2ed41c794753b9ea27da98b48713ed07a974b4d71273de541a9bfe94`.
- logs/helper-history-1794316633.tar.xz: SHA-256 `d19316e232d38452a2c5ca95ad7ccc9e7b218f0aedd7512739ab9eb9ca5c5b7c`.
- logs/helper-history-1794316771.tar.xz: SHA-256 `c2f67a39af198b0841e4d760af8974b9ccbcb57fba5edaa30ca6474e53765bb0`.
- logs/phase1-closed-logs-1794299803.tar.xz: SHA-256 `944f2fcf10db62ec8f436ac745a960b6804aac562842b6f81cb307eb3964963b`.
- logs/phase2-closed-logs-1794303266.tar.xz: SHA-256 `ec7fef0edc76f299b6e0516ed47e0ed629d5bd6053134de699ea8494506473e3`.
- logs/phase3-closed-logs-1794317370.tar.xz: SHA-256 `f2f12476b2abd838f931e7c753dcbea4a792e5715f3fcd8ef8968161c8367f86`.
- sources/final-source-bytes-1794317649.tar.xz: SHA-256 `296c0262c0244c22bba9068309f1c290a47126e6ce58a379dcdac90f8a0c0382`.
- sources/initial-source-bytes-1794296375.tar.xz: SHA-256 `6af0e962a0d5ab8c35930e9f19ad6bb0a4b5b91eab4dbe55cf4572bbde0bb628`.
- sources/initial-source-bytes-1794296444.tar.xz: SHA-256 `5878b614236d62d3d8a6ffba245c30fea212e0ded15ecb06838c0c73bdf31cf8`.
- sources/initial-source-bytes-1794317380.tar.xz: SHA-256 `39305f23fb3ab598a4d2eaedcdd107a0d8b30d62d6b55d9d4fe851b51e643e1a`.

Scheduling note: this release session inherited nice 15 and could not raise priority to absolute nice 10. Its measured replays ran at inherited nice 15, a lower CPU priority. The commands above request nice 10 from a normal-priority shell.
