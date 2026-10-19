var addressMarker = null;
var addressSearchVersion = 0;
var displayedTongData = null;

function pointInRing(point, ring) {
  var inside = false;
  for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    var a = ring[j], b = ring[i];
    var cross = (point[0] - a[0]) * (b[1] - a[1]) - (point[1] - a[1]) * (b[0] - a[0]);
    if (Math.abs(cross) < 1e-12 && point[0] >= Math.min(a[0], b[0]) && point[0] <= Math.max(a[0], b[0]) && point[1] >= Math.min(a[1], b[1]) && point[1] <= Math.max(a[1], b[1])) return true;
    if ((a[1] > point[1]) !== (b[1] > point[1]) && point[0] < (b[0] - a[0]) * (point[1] - a[1]) / (b[1] - a[1]) + a[0]) inside = !inside;
  }
  return inside;
}

function findAddressDistrict(point, features) {
  var matches = [];
  features.forEach(function (feature) {
    if (!feature.rings.some(function (ring) { return pointInRing(point, ring); })) return;
    var bans = feature.banShapes.filter(function (ban) {
      return ban.rings.some(function (ring) { return pointInRing(point, ring); });
    });
    if (!bans.length) matches.push(feature.tong + '통 · 반 경계 미등록');
    bans.forEach(function (ban) { matches.push(feature.tong + '통 ' + ban.ban + '반'); });
  });
  return matches;
}

async function locateAddress(address, version) {
  var result = document.getElementById('addressResult');
  var point = [Number(address.x), Number(address.y)];
  var dongNames = Object.keys(ALL_DONG_BOUNDARIES).filter(function (name) {
    return pointInRing(point, boundaryRingFromData(ALL_DONG_BOUNDARIES[name]));
  });
  var position = new kakao.maps.LatLng(point[1], point[0]);
  if (addressMarker) addressMarker.setMap(null);
  addressMarker = new kakao.maps.Marker({ map: oMap, position: position });
  oMap.setLevel(3);
  oMap.panTo(position);
  if (!dongNames.length) { result.textContent = '용산구 경계 밖의 주소입니다.'; return; }
  result.textContent = '통·반 확인 중…';
  try {
    var groups = await Promise.all(dongNames.map(async function (name) {
      var data;
      if (name === document.getElementById('dongBoundarySelect').value) data = displayedTongData;
      else data = await fetchRemoteTongData(name) || SAVED_TONG_DATA[name];
      return { name: name, data: data, matches: findAddressDistrict(point, tongFeaturesFromData(data)) };
    }));
    if (version !== addressSearchVersion) return;
    var matches = [];
    groups.forEach(function (group) { group.matches.forEach(function (match) { matches.push(group.name + ' ' + match); }); });
    result.textContent = matches.length ? matches.join(' / ') + (matches.length > 1 ? ' · 경계에 걸친 위치입니다.' : '') : dongNames.join(' / ') + ' · 해당 위치의 통·반 경계가 등록되지 않았습니다.';
    var group = groups.find(function (entry) { return entry.matches.length; }) || groups[0];
    document.getElementById('dongBoundarySelect').value = group.name;
    BOUNDARY_DATA = ALL_DONG_BOUNDARIES[group.name];
    TONG_DATA = group.data || emptyTongData(group.name);
    renderAll(TONG_DATA, BOUNDARY_DATA);
    oMap.setLevel(3);
    oMap.panTo(position);
  } catch (error) {
    if (version === addressSearchVersion) result.textContent = '경계를 확인하지 못했습니다. 다시 검색해주세요.';
  }
}

document.getElementById('addressForm').addEventListener('submit', function (event) {
  event.preventDefault();
  var query = document.getElementById('addressInput').value.trim();
  var result = document.getElementById('addressResult');
  var choices = document.getElementById('addressChoices');
  var version = ++addressSearchVersion;
  choices.replaceChildren();
  if (!query) { result.textContent = '주소를 입력해주세요.'; return; }
  if (!oMap || !window.kakao || !kakao.maps.services) { result.textContent = '지도를 불러온 뒤 다시 검색해주세요.'; return; }
  result.textContent = '검색 중…';
  new kakao.maps.services.Geocoder().addressSearch(query, function (addresses, status) {
    if (version !== addressSearchVersion) return;
    if (status !== kakao.maps.services.Status.OK || !addresses.length) { result.textContent = '주소를 찾지 못했습니다. 동 이름과 번지를 확인해주세요.'; return; }
    if (addresses.length === 1) { locateAddress(addresses[0], version); return; }
    result.textContent = '주소를 선택해주세요.';
    addresses.forEach(function (address) {
      var button = document.createElement('button');
      button.type = 'button';
      button.textContent = (address.road_address && address.road_address.address_name) || address.address_name;
      button.addEventListener('click', function () { choices.replaceChildren(); locateAddress(address, version); });
      choices.appendChild(button);
    });
  });
});
