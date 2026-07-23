# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0](https://github.com/kadeschs/robovacl60/compare/v1.3.1...v1.4.0) (2026-07-23)


### Features

* Migrate to v2 API ([#68](https://github.com/kadeschs/robovacl60/issues/68)) ([1b909cc](https://github.com/kadeschs/robovacl60/commit/1b909cc910a59290e1fba8814c194626c82cc377))
* rewrite network code to make it more linear and handle being offline better ([88ef4a6](https://github.com/kadeschs/robovacl60/commit/88ef4a6e25d886d5d4991623cd4f7493752f59d6))
* update node.js to v22.17.0 ([#132](https://github.com/kadeschs/robovacl60/issues/132)) ([e1b81fa](https://github.com/kadeschs/robovacl60/commit/e1b81fa84939310e693f5ea094b651330c8f51d9))
* Update workflows ([#56](https://github.com/kadeschs/robovacl60/issues/56)) ([04a855e](https://github.com/kadeschs/robovacl60/commit/04a855eb65c6858ec451e3e4e7c753f227c5adb0))


### Bug Fixes

* (refactor) replace TUYA_CODES references with TuyaCodes class ([#141](https://github.com/kadeschs/robovacl60/issues/141)) ([5eabac6](https://github.com/kadeschs/robovacl60/commit/5eabac65ddf1a0d35ce5eb018c12e861e077b1b8))
* add better logging when unexpected error is recieved during config ([79892aa](https://github.com/kadeschs/robovacl60/commit/79892aa98f696cd697dba52ff2931d4b116c0b16))
* Add custom vaccums ([#53](https://github.com/kadeschs/robovacl60/issues/53)) ([4753e4d](https://github.com/kadeschs/robovacl60/commit/4753e4d6101bc67f9787afd285a0b14c3ab88ab4))
* add extra logging ([3dd4a7b](https://github.com/kadeschs/robovacl60/commit/3dd4a7b0e093c625029b14c82c28b3b6c9181c27))
* Add friendly heredocs to files so that we can all find models easier ([#86](https://github.com/kadeschs/robovacl60/issues/86)) ([604c403](https://github.com/kadeschs/robovacl60/commit/604c40394f2fab5920398ddca51caa61aa6c8537))
* add manual trigger for release workflow ([a65a0f2](https://github.com/kadeschs/robovacl60/commit/a65a0f2a72dd11956d9eba6f9eba9a4496265f6d))
* add more routes for trying to find the tuya region ([2968d72](https://github.com/kadeschs/robovacl60/commit/2968d722f8c34d892ab5cf2df107e90002c7e1be))
* Add T2267 and T2268 (L60 and L60 Hybrid) ([#81](https://github.com/kadeschs/robovacl60/issues/81)) ([aad9330](https://github.com/kadeschs/robovacl60/commit/aad93304934fba988117a8bab0f6d87b19aecc9d))
* adjust times for refresh, ping and timeout ([96a155d](https://github.com/kadeschs/robovacl60/commit/96a155d3782fb3f612a810ed3723e71b63c31469))
* Allow 2 blank lines in markdown ([#62](https://github.com/kadeschs/robovacl60/issues/62)) ([3ec9117](https://github.com/kadeschs/robovacl60/commit/3ec9117d2dcf155dcbd7dc0f20936b76bee1de0e))
* Also bump the version in manifest.json ([#71](https://github.com/kadeschs/robovacl60/issues/71)) ([64b1f6b](https://github.com/kadeschs/robovacl60/commit/64b1f6ba8b0d6f1f31171d37eb9402fc2cd2b1d0))
* Codecov ([#65](https://github.com/kadeschs/robovacl60/issues/65)) ([10ccbda](https://github.com/kadeschs/robovacl60/commit/10ccbdaa85a7839edd21d00595c9bd249736aa35))
* correct release-please manifest path for robovacl60 integration ([2e4de3e](https://github.com/kadeschs/robovacl60/commit/2e4de3ea3fdd3e62150c739b0a93448d1e11fc2a))
* fan speed list for T2181 ([#87](https://github.com/kadeschs/robovacl60/issues/87)) ([0f64f72](https://github.com/kadeschs/robovacl60/commit/0f64f7234f03a81593e928e55f15c49a56d7b206))
* Fix init arguments in robovac ([#77](https://github.com/kadeschs/robovacl60/issues/77)) ([7d3c5df](https://github.com/kadeschs/robovacl60/commit/7d3c5df81cb543308483516c91cf0d1cb23ddc80))
* fix reference to incorrect key ([c687f11](https://github.com/kadeschs/robovacl60/commit/c687f111ebc81abddab2a50b8dc973c4bf04d634))
* Fix return types from RoboVac ([#72](https://github.com/kadeschs/robovacl60/issues/72)) ([f9fb413](https://github.com/kadeschs/robovacl60/commit/f9fb413a474048ff4d1528c74586ab8e5ff65063))
* fixed issue with multiple ping loops running ([3e2b923](https://github.com/kadeschs/robovacl60/commit/3e2b9232553e4a3765826925dfb0948573b210ca))
* force disconnect on connection reset ([c251501](https://github.com/kadeschs/robovacl60/commit/c251501aed647f9d8757ae8a4545c484aafc56e8))
* log eufy device info when device not found on tuya ([f397319](https://github.com/kadeschs/robovacl60/commit/f39731907054dba113b92e95845dfe554316af82))
* missed underscores 🤦‍♂️ ([ac0dbdd](https://github.com/kadeschs/robovacl60/commit/ac0dbdd11a0d4b325619682bf26e2f8e6ac9da64))
* print stack trace on connection reset ([2c741fe](https://github.com/kadeschs/robovacl60/commit/2c741fe32e3ac76a24214306452e6b7f7ed9b14b))
* Refactor DPS codes ([#106](https://github.com/kadeschs/robovacl60/issues/106)) ([f96fef0](https://github.com/kadeschs/robovacl60/commit/f96fef0d09f78b41936c7581dce229182db6feb8))
* Replcae codefoodpixels references for damacus ([#2](https://github.com/kadeschs/robovacl60/issues/2)) ([a0b215c](https://github.com/kadeschs/robovacl60/commit/a0b215c3243916993d9376839f74ffa035475ee9))
* send eof to reader when disconnecting ([0b18494](https://github.com/kadeschs/robovacl60/commit/0b18494fb1842df7adfd2d83acd332f3307b54a0))
* Update README.md ([#25](https://github.com/kadeschs/robovacl60/issues/25)) ([5ba8d4c](https://github.com/kadeschs/robovacl60/commit/5ba8d4cad1742a32e3cd35af422ec67f2faa8887))
* use built-in GITHUB_TOKEN instead of GitHub App ([2b9e61c](https://github.com/kadeschs/robovacl60/commit/2b9e61c1c257cb440434469d92b60725ec960f44))
* use model-specific code for start commands ([#139](https://github.com/kadeschs/robovacl60/issues/139)) ([f83f29e](https://github.com/kadeschs/robovacl60/commit/f83f29eb194158a478b421abbeb217420037c1cb))

## [1.3.1](https://github.com/damacus/robovac/compare/v1.3.0...v1.3.1) (2025-07-05)


### Bug Fixes

* (refactor) replace TUYA_CODES references with TuyaCodes class ([#141](https://github.com/damacus/robovac/issues/141)) ([5eabac6](https://github.com/damacus/robovac/commit/5eabac65ddf1a0d35ce5eb018c12e861e077b1b8))
* use model-specific code for start commands ([#139](https://github.com/damacus/robovac/issues/139)) ([f83f29e](https://github.com/damacus/robovac/commit/f83f29eb194158a478b421abbeb217420037c1cb))

## [1.3.0](https://github.com/damacus/robovac/compare/v1.2.5...v1.3.0) (2025-07-02)


### Features

* update node.js to v22.17.0 ([#132](https://github.com/damacus/robovac/issues/132)) ([e1b81fa](https://github.com/damacus/robovac/commit/e1b81fa84939310e693f5ea094b651330c8f51d9))

## [1.2.5](https://github.com/damacus/robovac/compare/v1.2.4...v1.2.5) (2025-06-24)


### Bug Fixes

* Refactor DPS codes ([#106](https://github.com/damacus/robovac/issues/106)) ([f96fef0](https://github.com/damacus/robovac/commit/f96fef0d09f78b41936c7581dce229182db6feb8))

## [1.2.4](https://github.com/damacus/robovac/compare/v1.2.3...v1.2.4) (2025-05-21)


### Bug Fixes

* fan speed list for T2181 ([#87](https://github.com/damacus/robovac/issues/87)) ([0f64f72](https://github.com/damacus/robovac/commit/0f64f7234f03a81593e928e55f15c49a56d7b206))

## [1.2.3](https://github.com/damacus/robovac/compare/v1.2.2...v1.2.3) (2025-05-13)


### Bug Fixes

* Add friendly heredocs to files so that we can all find models easier ([#86](https://github.com/damacus/robovac/issues/86)) ([604c403](https://github.com/damacus/robovac/commit/604c40394f2fab5920398ddca51caa61aa6c8537))
* Add T2267 and T2268 (L60 and L60 Hybrid) ([#81](https://github.com/damacus/robovac/issues/81)) ([aad9330](https://github.com/damacus/robovac/commit/aad93304934fba988117a8bab0f6d87b19aecc9d))

## [1.2.2](https://github.com/damacus/robovac/compare/v1.2.1...v1.2.2) (2025-05-07)


### Bug Fixes

* Fix init arguments in robovac ([#77](https://github.com/damacus/robovac/issues/77)) ([7d3c5df](https://github.com/damacus/robovac/commit/7d3c5df81cb543308483516c91cf0d1cb23ddc80))

## [1.2.1](https://github.com/damacus/robovac/compare/v1.2.0...v1.2.1) (2025-05-07)


### Bug Fixes

* Also bump the version in manifest.json ([#71](https://github.com/damacus/robovac/issues/71)) ([64b1f6b](https://github.com/damacus/robovac/commit/64b1f6ba8b0d6f1f31171d37eb9402fc2cd2b1d0))
* Fix return types from RoboVac ([#72](https://github.com/damacus/robovac/issues/72)) ([f9fb413](https://github.com/damacus/robovac/commit/f9fb413a474048ff4d1528c74586ab8e5ff65063))

## [1.2.0](https://github.com/damacus/robovac/compare/v1.1.0...v1.2.0) (2025-05-07)


### Features

* Migrate to v2 API ([#68](https://github.com/damacus/robovac/issues/68)) ([1b909cc](https://github.com/damacus/robovac/commit/1b909cc910a59290e1fba8814c194626c82cc377))

## [1.1.0](https://github.com/damacus/robovac/compare/v1.0.2...v1.1.0) (2025-05-07)


### Features

* Update workflows ([#56](https://github.com/damacus/robovac/issues/56)) ([04a855e](https://github.com/damacus/robovac/commit/04a855eb65c6858ec451e3e4e7c753f227c5adb0))


### Bug Fixes

* Add custom vaccums ([#53](https://github.com/damacus/robovac/issues/53)) ([4753e4d](https://github.com/damacus/robovac/commit/4753e4d6101bc67f9787afd285a0b14c3ab88ab4))
* Allow 2 blank lines in markdown ([#62](https://github.com/damacus/robovac/issues/62)) ([3ec9117](https://github.com/damacus/robovac/commit/3ec9117d2dcf155dcbd7dc0f20936b76bee1de0e))
* Codecov ([#65](https://github.com/damacus/robovac/issues/65)) ([10ccbda](https://github.com/damacus/robovac/commit/10ccbdaa85a7839edd21d00595c9bd249736aa35))

## [Unreleased]
