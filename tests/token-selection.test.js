const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const action = fs.readFileSync(path.join(__dirname, '..', 'action.yml'), 'utf8');
const deployStep = action.split('- name: Deploy to GitHub Pages')[1];
assert.ok(deployStep, 'deploy step must exist');
const match = deployStep.match(/^\s+github_token:\s+\$\{\{\s*(.*?)\s*\}\}/m);
assert.ok(match, 'deploy step must pass a github_token expression');
const expression = match[1];

// These expressions use string inputs and operators shared by JavaScript and Actions.
for (const [externalRepository, personalToken, githubToken, expected] of [
  ['', '', 'built-in-token', 'built-in-token'],
  ['', '', 'custom-token', 'custom-token'],
  ['', '', '', ''],
  ['', 'personal-token', 'built-in-token', ''],
  ['', 'personal-token', 'custom-token', ''],
  ['', 'personal-token', '', ''],
  ['owner/repo', 'personal-token', 'built-in-token', ''],
  ['owner/repo', 'personal-token', 'custom-token', ''],
  ['owner/repo', 'personal-token', '', ''],
  ['owner/repo', '', 'built-in-token', ''],
]) {
  test(`github_token with external=${Boolean(externalRepository)}, personal=${Boolean(personalToken)} and github=${githubToken || 'empty'}`, () => {
    assert.equal(vm.runInNewContext(expression, {
      inputs: {external_repository: externalRepository, personal_token: personalToken, github_token: githubToken},
    }), expected);
  });
}

test('external deployments without a personal token fail early', () => {
  const validation = action.split('- name: Validate deployment credentials')[1]
    ?.split('- name: Set up Node.js')[0];
  assert.ok(validation, 'credential validation must precede the build');
  const condition = validation.match(/^\s+if:\s+\$\{\{\s*(.*?)\s*\}\}/m);
  assert.ok(condition, 'credential validation must have a condition');
  for (const [externalRepository, personalToken, expected] of [
    ['', '', false],
    ['', 'personal-token', false],
    ['owner/repo', '', true],
    ['owner/repo', 'personal-token', false],
  ]) {
    assert.equal(vm.runInNewContext(condition[1], {
      inputs: {external_repository: externalRepository, personal_token: personalToken},
    }), expected);
  }
  assert.match(validation, /::error::personal_token is required when external_repository is set\./);
  assert.match(validation, /exit 1/);
});

test('deploy step forwards the personal token', () => {
  assert.match(deployStep, /^\s+personal_token:\s+\$\{\{\s*inputs\.personal_token\s*\}\}/m);
});
