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
for (const [personalToken, githubToken, expected] of [
  ['', 'built-in-token', 'built-in-token'],
  ['', 'custom-token', 'custom-token'],
  ['', '', ''],
  ['personal-token', 'built-in-token', ''],
  ['personal-token', 'custom-token', ''],
  ['personal-token', '', ''],
]) {
  test(`github_token with personal=${Boolean(personalToken)} and github=${githubToken || 'empty'}`, () => {
    assert.equal(vm.runInNewContext(expression, {
      inputs: {personal_token: personalToken, github_token: githubToken},
    }), expected);
  });
}

test('deploy step forwards the personal token', () => {
  assert.match(deployStep, /^\s+personal_token:\s+\$\{\{\s*inputs\.personal_token\s*\}\}/m);
});
