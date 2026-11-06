console.log('현재 Frontend Origin:', window.location.origin);

async function loadMembers() {
  try {
    const response = await fetch(`${API_BASE_URL}/members/`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const members = await response.json();
    console.log(members);
  } catch (error) {
    console.error(error);
  }
}

loadMembers();

async function createMember(member) {
  const response = await fetch(`${API_BASE_URL}/members/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(member),
  });

  const body = await response.json();

  if (!response.ok) {
        throw new Error(
      typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail)
    );
  }

  return body;
}