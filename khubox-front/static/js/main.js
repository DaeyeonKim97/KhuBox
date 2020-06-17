$(document).ready(function(){ProcessHash();});
$(window).on('hashchange',function(){ProcessHash();});

$("body").on('dblclick', 'tr.single-file', function(e) {
  location.hash = `#!/files/${e.currentTarget.id}`;
});

const ProcessHash = () => {
  $('#card-1').hide();
  $('#card-2').hide();
  $('#card-3').hide();
  $('#card-4').hide();
  $('#card-5').hide();

  $('#menu-me').removeClass('active');
  $('#menu-public').removeClass('active');
  $('#menu-starred').removeClass('active');
  $('#menu-trash').removeClass('active');
  $('#folder_name').text('');
  $('#folder_id').hide();
  $('#menu-top-me').hide();
  $('#menu-top-group').hide();
  $('#menu-top-trash').hide();
  $('#main-1').hide();
  $('#main-2').hide();
  $('#login').hide();
  $('#register').hide();
  $('html').removeClass('login-html');
  $('body').removeClass('login-body');
  $('body').removeClass('text-center');
  if (location.hash === '#!/login') {
    $('html').addClass('login-html');
    $('body').addClass('login-body');
    $('body').addClass('text-center')
    $('#login').show();
  } else if (location.hash === '#!/register') {
    $('html').addClass('login-html');
    $('body').addClass('login-body');
    $('body').addClass('text-center')
    $('#register').show();
  } else if (location.hash === '#!/logout') {
    localStorage.clear();
    location.hash = '#!/login';
  } else if (location.hash === '#!/settings') {
    // TODO
    ProcessMain();
    $('#main-1').show();
    $('#main-2').show();
  } else if (location.hash === '#!/public') {
    ProcessMain();
    $('#main-1').show();
    $('#main-2').show();
    GetPublicList();
    $('#folder_name').text('공유한 파일');
    $('#menu-public').show();
    $('#file_list').show();
  } else if (location.hash === '#!/starred') {
    ProcessMain();
    $('#main-1').show();
    $('#main-2').show();
    GetStarredList();
    $('#folder_name').text('중요 문서함');
    $('#menu-starred').show();
    $('#file_list').show();
  } else if (location.hash === '#!/trash') {
    ProcessMain();
    $('#main-1').show();
    $('#main-2').show();
    GetTrashList();
    $('#folder_name').text('휴지통');
    $('#menu-top-trash').show();
    $('#file_list').show();
  } else if (location.hash === '#!/add-group') {
    ProcessMain();
    $('#main-1').show();
    $('#main-2').show();
    $('#add_group').show();
  } else if (location.hash.indexOf('#!/groups/') > -1) {
    ProcessMain();
    $('#main-1').show();
    $('#main-2').show();
    $('#manage_group').show();
    ProcessGroup();
  } else if (location.hash.indexOf('#!/files/') > -1) {
    ProcessMain();
    $('#main-1').show();
    $('#main-2').show();
    GetFileLis(location.hash.substring(9));
    $('#file_list').show();
  } else {
    const token = localStorage.getItem('token');
    if (token === null) {
      location.hash = '#!/login';
    } else {
      location.hash = `#!/files/${localStorage.getItem('root_folder')}`;
    }
  }
  feather.replace();
}

const GetFileLis = (file_id) => {
  $('#file_items').empty();
  $.ajax({
    url: `https://khubox-api.khunet.net/files/${file_id}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'GET',
    success: (response) => {
      if (response.result === true) {
        if (response.data.parent_id === null) {
          const current_id = location.hash.substring(9);
          const me_root_folder = localStorage.getItem('root_folder');

          if (current_id === me_root_folder) {
            $('#menu-top-me').show();
            $('#menu-me').addClass('active');
            $('#folder_name').text('내 파일');
            $('#folder_id').show();
            $('#folder_id').text(`폴더ID : ${me_root_folder}`);
          } else {
            // 그룹
            $('#menu-top-group').show();
          }
        } else {
          $('#menu-top-me').show();
          $('#folder_name').text(response.data.name);
          $('#folder_id').show();
          $('#folder_id').text(`폴더ID : ${response.data.id}`);
          $('#file_items').append(`
                    <tr class="single-file" id="${response.data.parent_id}">
                        <td>
                            <span data-feather="folder"></span>
                            ..
                        </td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
          `);
        }

        if (response.data.download_url) {
          location.href = response.data.download_url;
          return;
        }

        const s_folders = response.files.filter(x => x.type === 'folder');
        const s_files = response.files.filter(x => x.type === 'file');
        for (const single of s_folders) {
          $('#file_items').append(`
                    <tr class="single-file" id="${single.id}">
                        <td>
                            <span data-feather="folder"></span>
                            ${single.name}
                            ${(single.is_starred === 1)?'<span data-feather="star"></span>':''}
                            ${(single.is_public === 1)?'<span data-feather="share-2"></span>':''}
                        </td>
                        <td>${single.created_at}</td>
                        <td></td>
                        <td>
                            <div class="dropdown">
                                <span class="badge badge-primary px-2" type="button" data-toggle="dropdown" data-boundary="viewport">
                                    <span data-feather="more-horizontal"></span>
                                </span>
                                <div class="dropdown-menu dropdown-menu-right">
                                    ${(single.is_public === 0)?
            '<a class="dropdown-item" onclick="GoShare(\''+single.id+'\', true);">공유</a>':
            '<a class="dropdown-item" onclick="GoShareLink(\''+single.id+'\');">공유 링크 확인</a>' +
            '<a class="dropdown-item" onclick="GoShare(\''+single.id+'\', false);">공유 해제</a>'}
                                    <a class="dropdown-item" onclick="GoMove('${single.id}');">이동</a>
                                    ${(single.is_starred === 0)?
            '<a class="dropdown-item" onclick="GoStar(\''+single.id+'\', true);">중요 문서함에 추가</a>':
            '<a class="dropdown-item" onclick="GoStar(\''+single.id+'\', false);">중요 문서함에서 삭제</a>'}
                                    <a class="dropdown-item" onclick="GoRename('${single.id}', '${single.name}');">이름 바꾸기</a>
                                    <a class="dropdown-item" onclick="GoDelete('${single.id}');">삭제</a>
                                </div>
                            </div>
                        </td>
                    </tr>
          `);
        }
        for (const single of s_files) {
          $('#file_items').append(`
                    <tr>
                        <td>
                            <span data-feather="file-text"></span>
                            ${single.name}
                            ${(single.is_starred === 1)?'<span data-feather="star"></span>':''}
                            ${(single.is_public === 1)?'<span data-feather="share-2"></span>':''}
                        </td>
                        <td>${single.created_at}</td>
                        <td>${single.size}</td>
                        <td>
                            <div class="dropdown">
                                <span class="badge badge-primary px-2" type="button" data-toggle="dropdown" data-boundary="viewport">
                                    <span data-feather="more-horizontal"></span>
                                </span>
                                <div class="dropdown-menu dropdown-menu-right">
                                    <a class="dropdown-item" onclick="GoDownload('${single.id}');">다운로드</a>
                                    ${(single.is_public === 0)?
            '<a class="dropdown-item" onclick="GoShare(\''+single.id+'\', true);">공유</a>':
            '<a class="dropdown-item" onclick="GoShareLink(\''+single.id+'\');">공유 링크 확인</a>' +
            '<a class="dropdown-item" onclick="GoShare(\''+single.id+'\', false);">공유 해제</a>'}
                                    <a class="dropdown-item" onclick="GoMove('${single.id}');">이동</a>
                                    ${(single.is_starred === 0)?
            '<a class="dropdown-item" onclick="GoStar(\''+single.id+'\', true);">중요 문서함에 추가</a>':
            '<a class="dropdown-item" onclick="GoStar(\''+single.id+'\', false);">중요 문서함에서 삭제</a>'}
                                    <a class="dropdown-item" onclick="GoRename('${single.id}', '${single.name}');">이름 바꾸기</a>
                                    <a class="dropdown-item" onclick="GoCopy('${single.id}');">사본 만들기</a>
                                    <a class="dropdown-item" onclick="GoDelete('${single.id}');">삭제</a>
                                </div>
                            </div>
                        </td>
                    </tr>
          `);
        }
        feather.replace();
      } else {
        alert(response.error);
      }
    }
  });
};
const GetTrashList = () => {
  $('#file_items').empty();
  $.ajax({
    url: `https://khubox-api.khunet.net/files?is_trashed=true`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'GET',
    success: (response) => {
      if (response.result === true) {
        $('#menu-trash').addClass('active');
        for (const single of response.data) {
          $('#file_items').append(`
                    <tr>
                        <td>
                            <span data-feather="${(single.type==='folder')?'folder':'file'}"></span>
                            ${single.name}
                            ${(single.is_starred === 1)?'<span data-feather="star"></span>':''}
                            ${(single.is_public === 1)?'<span data-feather="share-2"></span>':''}
                        </td>
                        <td>${single.created_at}</td>
                        <td></td>
                        <td>
                            <div class="dropdown">
                                <span class="badge badge-primary px-2" type="button" data-toggle="dropdown" data-boundary="viewport">
                                    <span data-feather="more-horizontal"></span>
                                </span>
                                <div class="dropdown-menu dropdown-menu-right">
                                    <a class="dropdown-item" onclick="GoRecover('${single.id}');">복원</a>
                                </div>
                            </div>
                        </td>
                    </tr>
          `);
        }
        feather.replace();
      } else {
        alert(response.error);
      }
    }
  });
};
const GetPublicList = () => {
  $('#file_items').empty();
  $.ajax({
    url: `https://khubox-api.khunet.net/files?is_public=true`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'GET',
    success: (response) => {
      if (response.result === true) {
        $('#menu-public').addClass('active');
        for (const single of response.data) {
          $('#file_items').append(`
                    <tr class="single-file" id="${(single.type==='folder')?single.id:single.parent_id}">
                        <td>
                            <span data-feather="${(single.type==='folder')?'folder':'file-text'}"></span>
                            ${single.name}
                            ${(single.is_starred === 1)?'<span data-feather="star"></span>':''}
                            ${(single.is_public === 1)?'<span data-feather="share-2"></span>':''}
                        </td>
                        <td>${single.created_at}</td>
                        <td>${(single.type==='file')?single.size:''}</td>
                        <td>
                            <div class="dropdown">
                                <span class="badge badge-primary px-2" type="button" data-toggle="dropdown" data-boundary="viewport">
                                    <span data-feather="more-horizontal"></span>
                                </span>
                                <div class="dropdown-menu dropdown-menu-right">
                                    ${(single.type==='file')?
            '<a class="dropdown-item" onclick="GoDownload(\''+single.id+'\');">다운로드</a>':''}
                                    ${(single.is_public === 0)?
            '<a class="dropdown-item" onclick="GoShare(\''+single.id+'\', true);">공유</a>':
            '<a class="dropdown-item" onclick="GoShareLink(\''+single.id+'\');">공유 링크 확인</a>' +
            '<a class="dropdown-item" onclick="GoShare(\''+single.id+'\', false);">공유 해제</a>'}
                                </div>
                            </div>
                        </td>
                    </tr>
          `);
        }
        feather.replace();
      } else {
        alert(response.error);
      }
    }
  });
};
const GetStarredList = () => {
  $('#file_items').empty();
  $.ajax({
    url: `https://khubox-api.khunet.net/files?is_starred=true`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'GET',
    success: (response) => {
      if (response.result === true) {
        $('#menu-starred').addClass('active');
        for (const single of response.data) {
          $('#file_items').append(`
                    <tr class="single-file" id="${(single.type==='folder')?single.id:single.parent_id}">
                        <td>
                            <span data-feather="${(single.type==='folder')?'folder':'file-text'}"></span>
                            ${single.name}
                            ${(single.is_starred === 1)?'<span data-feather="star"></span>':''}
                            ${(single.is_public === 1)?'<span data-feather="share-2"></span>':''}
                        </td>
                        <td>${single.created_at}</td>
                        <td>${(single.type==='file')?single.size:''}</td>
                        <td>
                            <div class="dropdown">
                                <span class="badge badge-primary px-2" type="button" data-toggle="dropdown" data-boundary="viewport">
                                    <span data-feather="more-horizontal"></span>
                                </span>
                                <div class="dropdown-menu dropdown-menu-right">
                                    ${(single.type==='file')?
            '<a class="dropdown-item" onclick="GoDownload(\''+single.id+'\');">다운로드</a>':''}
                                    ${(single.is_starred === 0)?
            '<a class="dropdown-item" onclick="GoStar(\''+single.id+'\', true);">중요 문서함에 추가</a>':
            '<a class="dropdown-item" onclick="GoStar(\''+single.id+'\', false);">중요 문서함에서 삭제</a>'}
                                </div>
                            </div>
                        </td>
                    </tr>
          `);
        }
        feather.replace();
      } else {
        alert(response.error);
      }
    }
  });
};

const GoShareLink = (file_id) => {
  $('#share-pop').append(`
            <div class="alert alert-info alert-dismissible fade show" role="alert">
                ${`https://khubox.khunet.net/#!/files/${file_id}`}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
  `);
}
const GoShare = (file_id, isBool) => {
  const post_data = {
    is_public: isBool,
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/files/${file_id}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'PATCH',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        location.reload();
      } else {
        alert(response.error)
      }
    }
  });
}
const GoMove = (file_id) => {
  $('#new-move-id').val(file_id);
  $('#modal-move').modal({
    show: true,
  });
}
const GoStar = (file_id, isBool) => {
  const post_data = {
    is_starred: isBool,
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/files/${file_id}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'PATCH',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        location.reload();
      } else {
        alert(response.error)
      }
    }
  });
}
const GoRename = (file_id, original_name) => {
  $('#new-rename').val(original_name);
  $('#new-rename-id').val(file_id);
  $('#modal-rename').modal({
    show: true,
  });
}
const GoCopy = (file_id) => {
  $.ajax({
    url: `https://khubox-api.khunet.net/files/${file_id}/copy`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'POST',
    success: (response) => {
      if (response.result === true) {
        location.reload();
      } else {
        alert(response.error)
      }
    }
  });
}
const GoDownload = (file_id) => {
  $.ajax({
    url: `https://khubox-api.khunet.net/files/${file_id}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'GET',
    success: (response) => {
      if (response.result === true) {
        window.open(response.data.download_url);
      } else {
        alert(response.error);
      }
    }
  });
}
const GoDelete = (file_id) => {
  const post_data = {
    is_trashed: true,
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/files/${file_id}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'PATCH',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        location.reload();
      } else {
        alert(response.error)
      }
    }
  });
}
const Rename = () => {
  const file_id = $('#new-rename-id').val();
  const name = $('#new-rename').val();
  const post_data = {
    name: name,
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/files/${file_id}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'PATCH',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        location.reload();
      } else {
        alert(response.error)
      }
    }
  });
};
const Move = () => {
  const file_id = $('#new-move-id').val();
  const parent_id = $('#new-folder').val();
  const post_data = {
    parent_id: parent_id,
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/files/${file_id}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'PATCH',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        location.reload();
      } else {
        alert(response.error)
      }
    }
  });
};
const GoNewFolder = () => {
  $('#modal-new-folder').modal({
    show: true,
  });
};
const CreateFolder = () => {
  const parent_id = location.hash.substring(9);
  const name = $('#new-folder-name').val();
  if (name === '') {
    alert('폴더명을 입력해주세요.');
    return;
  }
  const post_data = {
    parent_id: parent_id,
    type: 'folder',
    name: name,
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/files`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'POST',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        location.reload();
      } else {
        alert(response.error)
      }
    }
  });
}
const GoUpload = () => {
  $('#upload-file').trigger('click');
};
$('#upload-file').change(() => {
  const theFormFile = $('#upload-file').get()[0].files[0];
  if (theFormFile === undefined)
    return;

  const parent_id = location.hash.substring(9);
  const name = theFormFile.name;

  const post_data = {
    parent_id: parent_id,
    type: 'file',
    name: name,
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/files`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'POST',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        RealUpload(response.upload_url);
      } else {
        alert(response.error)
      }
    }
  });
});
const RealUpload = (upload_url) => {
  const theFormFile = $('#upload-file').get()[0].files[0];
  if (theFormFile === undefined)
    return;
  $('#upload-progress').show();
  $.ajax({
    xhr: function() {
      var xhr = new window.XMLHttpRequest();
      xhr.upload.addEventListener("progress", function(evt) {
        if (evt.lengthComputable) {
          var percentComplete = evt.loaded / evt.total;
          percentComplete = parseInt(percentComplete * 100);
          console.log(percentComplete);
          $('#progress-val').css('width', `${percentComplete}%`);
          if (percentComplete === 100) {
            location.reload();
          }
        }
      }, false);
      return xhr;
    },
    type: 'PUT',
    url: upload_url,
    contentType: 'application/octet-stream',
    processData: false,
    data: theFormFile,
    success: (response) => {

    }
  });
};
const ProcessMain = () => {
  $('#file_list').hide();
  $('#add_group').hide();
  $('#manage_group').hide();
  $('#file_items').empty();
  $('#group_list').empty();
  const groups = JSON.parse(localStorage.getItem('groups'));
  for (const group of groups) {
    if (location.hash.substring(9)===group.root_folder) {
      $('#folder_name').text(group.name);
      $('#folder_id').show();
      $('#folder_id').text(`폴더ID : ${group.root_folder}`);
      $('#btn-go-group').attr('onclick', `GoGroup('${group.id}');`);
    }
    $('#group_list').append(`
      <li class="nav-item">
        <a class="nav-link${(location.hash.substring(9)===group.root_folder)?' active':''}" href="#!/files/${group.root_folder}">
        <span data-feather="hard-drive"></span>
        ${group.name}
        </a>
      </li>
    `);
  }
};
const doLogin = () => {
  const post_data = {
    email: $('#login-email').val(),
    password: $('#login-password').val(),
  };
  $.ajax({
    url: 'https://khubox-api.khunet.net/users/login',
    type: 'POST',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        localStorage.setItem('token', response.token);
        getRootFolder();
      } else {
        alert(response.error)
      }
    }
  });
};
const getRootFolder = () => {
  $.ajax({
    url: 'https://khubox-api.khunet.net/users/me',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'GET',
    success: (response) => {
      if (response.result === true) {
        localStorage.setItem('root_folder', response.data.root_folder);
        getGroups();
      } else {
        alert(response.error);
      }
    }
  });
};
const getGroups = () => {
  $.ajax({
    url: 'https://khubox-api.khunet.net/groups/me',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'GET',
    success: (response) => {
      if (response.result === true) {
        localStorage.setItem('groups', JSON.stringify(response.data));
        location.hash = '#';
      } else {
        alert(response.error);
      }
    }
  });
};
const doRegister = () => {
  if ($('#register-password').val() !== $('#register-password_re').val()) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }
  const post_data = {
    email: $('#register-email').val(),
    password: $('#register-password').val(),
    name: $('#register-name').val(),
  };
  $.ajax({
    url: 'https://khubox-api.khunet.net/users',
    type: 'POST',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        alert('성공적으로 가입되었습니다.');
        location.hash = '#';
      } else {
        alert(response.error)
      }
    }
  });
};
const GoGroup = (group_id) => {
  location.href = `#!/groups/${group_id}`;
};
const GoRecover = (file_id) => {
  const post_data = {
    is_trashed: false,
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/files/${file_id}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'PATCH',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        location.reload();
      } else {
        alert(response.error)
      }
    }
  });
};
const EmptyTrash = () => {
  $.ajax({
    url: `https://khubox-api.khunet.net/files/trash`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'DELETE',
    success: (response) => {
      if (response.result === true) {
        location.reload();
      } else {
        alert(response.error)
      }
    }
  });
};
const GroupJoin = () => {
  const invite_code = $('#input-invite-code').val();
  $.ajax({
    url: `https://khubox-api.khunet.net/groups/invite/${invite_code}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'POST',
    success: (response) => {
      if (response.result === true) {
        alert('성공적으로 그룹에 가입되었습니다.');
        getGroups();
      } else {
        alert(response.error)
      }
    }
  });
};
const GroupCreate = () => {
  const post_data = {
    name: $('#input-group-name').val(),
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/groups`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'POST',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        alert('성공적으로 그룹에 생성되었습니다.');
        getGroups();
      } else {
        alert(response.error)
      }
    }
  });
};

const ChangeGroupName = () => {
  const post_data = {
    name: $('#change-group-name').val(),
  };
  $.ajax({
    url: `https://khubox-api.khunet.net/groups/${$('#this-group-id').val()}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'PATCH',
    data: JSON.stringify(post_data),
    success: (response) => {
      if (response.result === true) {
        alert('성공적으로 변경되었습니다.');
        getGroups();
      } else {
        alert(response.error)
      }
    }
  });
};

const ProcessGroup = () => {
  const group_id = location.hash.substring(10);
  $('#this-group-id').val(group_id);

  $.ajax({
    url: `https://khubox-api.khunet.net/groups/${group_id}`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    type: 'GET',
    success: (response) => {
      if (response.result === true) {
        $('#change-group-name').val(response.data.name);
        if (response.data.is_owner === true) {
          $('#group-invite-code').val(response.data.invite_code);
          $('#card-1').show();
          $('#card-2').show();
          // $('#card-3').show();
          // $('#card-5').show();
        } else {
          // $('#card-4').show();
        }

      } else {
        alert(response.error)
      }
    }
  });

};

const GroupExit = () => {
  //
  // $.ajax({
  //   url: 'https://khubox-api.khunet.net/users/me',
  //   headers: {
  //     'Authorization': `Bearer ${localStorage.getItem('token')}`,
  //   },
  //   type: 'GET',
  //   success: (response) => {
  //     if (response.result === true) {
  //
  //
  //       $.ajax({
  //         url: `https://khubox-api.khunet.net/groups/${$('#this-group-id').val()}/users/${response.data.id}`,
  //         headers: {
  //           'Authorization': `Bearer ${localStorage.getItem('token')}`,
  //         },
  //         type: 'DELETE',
  //         success: (response) => {
  //           if (response.result === true) {
  //             alert('성공적으로 탈퇴되었습니다.');
  //             getGroups();
  //           } else {
  //             alert(response.error)
  //           }
  //         }
  //       });
  //
  //
  //
  //     } else {
  //       alert(response.error);
  //     }
  //   }
  // });



};
